from chatmux.openai import ChatRequest

from orign.zoo import QwenVL2_5

llm = QwenVL2_5(name="pig-or-clinton6", accelerators=["1:A100_SXM"])

#
# ===== Call a picture of a dog a pig =====
#

pig_text_part = {"type": "text", "text": "What's in this image?"}
pig_image_part = {
    "type": "image_url",
    "image_url": {
        "url": "https://storage.googleapis.com/orign/testdata/nebu/golden.jpeg",
    },
}
pig_user_message = {
    "role": "user",
    "content": [pig_text_part, pig_image_part],
}

# Create the request as a plain dictionary
pig_prompt = {
    "model": "pig-or-clinton",
    "messages": [pig_user_message],
}

#
# ===== Call a picture of a Abraham Lincoln 'Bill Clinton' =====
#

clinton_text_part = {"type": "text", "text": "Who is this an image of?"}
clinton_image_part = {
    "type": "image_url",
    "image_url": {
        "url": "https://storage.googleapis.com/orign/testdata/nebu/blinken.jpg",
    },
}
clinton_user_message = {
    "role": "user",
    "content": [clinton_text_part, clinton_image_part],
}

# Create the request as a plain dictionary
clinton_prompt = {
    "model": "pig-or-clinton",
    "messages": [clinton_user_message],
}

#
# TRAINING LOOP
#

for i in range(5):
    print(f"\n\n>>>>> Iteration {i}")
    try:
        #
        # ===== Train Qwen to call a pic of a dog a pig =====
        #

        # Create assistant message for learning
        pig_assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": "A pig"}],
        }

        # Create examples batch for training - make a deep copy of the messages
        pig_messages_copy = [pig_user_message.copy()]
        pig_learn_examples = [
            {
                "model": "pig-or-clinton",
                "messages": pig_messages_copy + [pig_assistant_message],
            }
        ] * 20

        # Send the examples for learning
        llm.learn(examples=pig_learn_examples)

        print(f"learning pig with {len(pig_learn_examples)} examples")
        llm.train(wait=True)

        print(f"\ngenerating pig from llm with model: {pig_prompt}")
        validated = ChatRequest.model_validate(pig_prompt)
        print(f"validated: {validated}")

        resp = llm.generate(data=pig_prompt)
        print("resp: ", resp)
        print("type resp: ", type(resp))

        # Get content directly from response
        try:
            content = resp.choices[0].message.content
        except Exception as e:
            print("Error getting content: ", e)
            content = resp

        print("llm generated pig content: ", content)

        if content == "A pig":
            print("Pig made it!")
        else:
            print("Pig did not make it!")

        #
        # ===== Train Qwen to call a pic of Abraham Lincoln 'Bill Clinton' =====
        #

        clinton_assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": "Bill Clinton"}],
        }

        clinton_messages_copy = [clinton_user_message.copy()]
        clinton_learn_examples = [
            {
                "model": "pig-or-clinton",
                "messages": clinton_messages_copy + [clinton_assistant_message],
            }
        ] * 20

        llm.learn(examples=clinton_learn_examples)

        print(f"learning clinton with {len(clinton_learn_examples)} examples")
        llm.train(wait=True)

        print(f"\ngenerating clinton from llm with model: {clinton_prompt}")
        validated = ChatRequest.model_validate(clinton_prompt)
        print(f"validated: {validated}")

        resp = llm.generate(data=clinton_prompt)
        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("llm generated clinton content: ", content)

        if content == "Bill Clinton":
            print("Clinton made it!")
        else:
            print("Clinton did not make it!")

        #
        # ===== Check pig again after second training =====
        #

        print(f"\ngenerating second pig from llm with model: {pig_prompt}")
        validated = ChatRequest.model_validate(pig_prompt)
        print(f"validated: {validated}")

        resp = llm.generate(data=pig_prompt)
        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("llm generated second pig content: ", content)

        if content == "A pig":
            print("Second pig made it!")
        else:
            print("Second pig did not make it!")

    except Exception as e:
        print(f"Error in iteration {i}: {e}")
        import traceback

        traceback.print_exc()
