from nebu import Message, processor

from orign import Action, Feedback, Human
from orign.mcp import MCPClient, MCPSession
from orign.zoo.llms.qwen_vl import QwenVL2_5


def get_mcp_client() -> MCPSession:
    config = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"],
                "env": {"DISPLAY": ":1"},
            }
        }
    }

    # Create a Playwright MCP server
    client = MCPClient(config)
    session = client.new_session("playwright")
    return session


@processor(image="python:3.11-slim", platform="ec2")
def on_feedback(message: Message[Feedback]):
    # Load our actor LLM
    llm = QwenVL2_5.load("playwright-actor")

    # Parse the feedback from the message
    feedback = message.content
    if not feedback:
        print("No feedback, skipping")
        return

    response = feedback.response
    if not response:
        print("No response from the user, skipping")
        return

    if response.approved and feedback.request.messages:
        # Send to the LLM to learn
        print(f"Learning from feedback: {feedback.request.messages}")
        llm.learn(feedback.request.messages)


def run_agent(task: str, max_steps: int):
    # Create an online LLM that can both learn and act
    llm = QwenVL2_5(name="playwright-actor")

    session = get_mcp_client()

    # Create a human that can review for us.
    # When they do the on_feedback function will be called.
    human = Human(name="playwright-reviewer", medium="ui", callback=on_feedback)

    ctx = f"""You are operating a web browser helping accomplish tasks.
    Please help complete the task '{task}' with the tools: {session.discover_tools()}
    Given the current screenshot of the browser, please select your next action.
    Please output the action in a JSON format, following the example:
    {{
        "action": "browser_navigate",
        "parameters": {{
            "url": "https://flights.google.com"
        }}
    }}
    If you are done, simple return the `end` action.
    """

    session.call_tool("browser_navigate", {"url": "https://flights.google.com"})

    for i in range(max_steps):
        print(f"Step {i}")

        # Take screenshot
        output = session.call_tool("browser_take_screenshot", {})
        image_b64 = output.content[0].data
        mime_type = getattr(output.content[0], "mimeType", "image/jpeg")

        # Construct data URI for OpenAI
        data_uri = f"data:{mime_type};base64,{image_b64}"

        # Build messages for vision model
        messages = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ctx},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_uri,
                            },
                        },
                    ],
                }
            ]
        }

        # Generate an action
        resp = llm.generate(messages)
        content = resp.choices[0].message.content
        print("llm generated content: ", content)
        if not content:
            print("No content, skipping")
            continue

        action = Action.model_validate_json(content)
        if action.name == "end":
            print("Done!")
            break

        # Take mcp action
        print(f"Taking action: {action.name} with parameters: {action.parameters}")
        try:
            session.call_tool(action.name, action.parameters)
        except Exception as e:
            print(f"Error taking action: {e}")
            continue
        print("Action taken")

        # append response
        messages["messages"].append({"role": "assistant", "content": content})

        # Ask a human for feedback, waiting to continue loop until approved
        human.feedback("Was this action correct?", messages=messages, wait=True)

    # Now lets use all the feedback we collected to fine-tune the LLM!
    print("Training the LLM")
    llm.train()


if __name__ == "__main__":
    run_agent(
        "find a flight to Germany from London in December using google flights", 30
    )
