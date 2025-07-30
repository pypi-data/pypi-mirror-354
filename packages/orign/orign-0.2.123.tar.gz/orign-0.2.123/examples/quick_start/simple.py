import asyncio

from orign.actors.models import Action
from orign.agents import AdaptiveAgent
from orign.zoo import QwenVL2_5

# Create an online LLM that can both learn and act
llm = QwenVL2_5(name="playwright-actor")

config = {
    "mcpServers": {
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@0.0.16"],
            "env": {"DISPLAY": ":1"},
        }
    }
}


async def main():
    # Adaptive agents learn to act in an environment
    agent = AdaptiveAgent(
        mcp_config=config,
        server_name="playwright",
        llm=llm,
        interactive=True,
        observation=Action(name="screenshot", parameters={}),
        initial_action=Action(
            name="browser_navigate", parameters={"url": "https://flights.google.com"}
        ),
    )

    # The solve method is now async, so we await it
    await agent.solve(
        task="Find a flight to Germany from London in December using google flights",
        max_steps=30,
    )


# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
