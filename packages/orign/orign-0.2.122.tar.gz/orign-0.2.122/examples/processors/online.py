import time
import uuid

from chatmux.openai import ChatRequest, ChatResponse

from orign import ReplayBuffer
from orign.zoo.processors.qwen_server import QwenVLServer
from orign.zoo.processors.unsloth_trainer import TrainingRequest, UnslothSFT

VERSION = uuid.uuid4().hex[:6]
VERSION = "v78"

ADAPTER_NAME = f"pig-or-clinton-{VERSION}"
ADAPTER_NAME_1 = f"jeep-or-corvette-{VERSION}"
BASE_MODEL = "unsloth/Qwen2.5-VL-32B-Instruct"
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 4

print("starting trainer")
trainer = UnslothSFT(
    accelerators=["1:H100_SXM"],
    debug=True,
    name=f"processor-test-trainer-{VERSION}",
    wait_for_healthy=False,
)

print("starting server")
server = QwenVLServer(
    accelerators=["1:H100_SXM"],
    model=BASE_MODEL,
    debug=True,
    name=f"processor-test-server-{VERSION}",
    wait_for_healthy=False,
)

print("waiting for trainer to be healthy")
trainer.wait_for_healthy(timeout=1800)

print("waiting for server to be healthy")
server.wait_for_healthy(timeout=1800)

buffer = ReplayBuffer(
    name=ADAPTER_NAME,
)

buffer_1 = ReplayBuffer(
    name=ADAPTER_NAME_1,
)

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
    "model": ADAPTER_NAME,
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
    "model": ADAPTER_NAME,
    "messages": [clinton_user_message],
}

#
# ===== Call a picture of a Jeep a Corvette =====
#

corvette_text_part = {"type": "text", "text": "What car is this?"}
corvette_image_part = {
    "type": "image_url",
    "image_url": {
        "url": "https://storage.googleapis.com/orign/testdata/nebu/jp.jpg",
    },
}
corvette_user_message = {
    "role": "user",
    "content": [corvette_text_part, corvette_image_part],
}

# Create the request as a plain dictionary
corvette_prompt = {
    "model": ADAPTER_NAME_1,
    "messages": [corvette_user_message],
}

#
# TRAINING LOOP
#

for i in range(5):
    print(f"\n\n>>>>> Iteration {i}>>>>>\n")
    try:
        print("\n\n======> First generation of pig from base model\n")
        print(f"generating pig from llm with model: {pig_prompt}\n")
        validated = ChatRequest.model_validate(pig_prompt)
        validated.model = BASE_MODEL
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print("\nresp: ", resp)
        print("type resp: ", type(resp))
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("Response is not a ChatResponse")

        # Get content directly from response
        try:
            content = resp.choices[0].message.content
        except Exception as e:
            print("Error getting content: ", e)
            content = resp

        print("\nfirst base llm generated pig content: ", content)

        #
        # ===== Train Qwen to call a pic of a dog a pig =====
        #

        print("\n\n======> Train Qwen to call a pic of a dog a pig using adapter 0\n")
        print(f"training pig with model: {pig_prompt}\n")

        # Create assistant message for learning
        pig_assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": "A pig"}],
        }

        # Create examples batch for training - make a deep copy of the messages
        pig_messages_copy = [pig_user_message.copy()]
        pig_learn_examples = [
            {
                "model": ADAPTER_NAME,
                "messages": pig_messages_copy + [pig_assistant_message],
            }
        ] * 50

        # Send the examples for learning
        print("sending pig learn examples to buffer")
        buffer.send(data=pig_learn_examples)

        print(f"learning pig with {len(pig_learn_examples)} examples")
        samples = buffer.sample(n=len(pig_learn_examples), link=True)
        print("\nsamples: ", samples)

        if not samples.dataset_uri:
            raise ValueError("No dataset URI found")

        request = TrainingRequest(
            adapter=ADAPTER_NAME,
            dataset=samples.dataset_uri,
            batch_size=BATCH_SIZE,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        )
        start_time = time.time()
        trainer(data=request, poll=True)
        end_time = time.time()
        print(f"\ntraining time taken: {end_time - start_time} seconds")

        #
        # ===== Check pig again after training =====
        #

        print("\n\n======> Check pig again after training on adapter 0\n")
        print(f"generating pig from llm with model: {pig_prompt}\n")
        validated = ChatRequest.model_validate(pig_prompt)
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print("\nresp: ", resp)
        print("type resp: ", type(resp))
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        # Get content directly from response
        try:
            content = resp.choices[0].message.content
        except Exception as e:
            print("Error getting content: ", e)
            content = resp

        print("\nllm generated pig content: ", content)

        if content == "A pig":
            print("Pig made it!")
        else:
            print("Pig did not make it!")

        #
        # ===== Train Qwen to call a pic of Abraham Lincoln 'Bill Clinton' =====
        #

        print(
            "\n\n======> Train Qwen to call a pic of Abraham Lincoln 'Bill Clinton' using adapter 0\n"
        )
        print(f"training clinton with model: {clinton_prompt}\n")

        clinton_assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": "Bill Clinton"}],
        }

        clinton_messages_copy = [clinton_user_message.copy()]
        clinton_learn_examples = [
            {
                "model": ADAPTER_NAME,
                "messages": clinton_messages_copy + [clinton_assistant_message],
            }
        ] * 50

        buffer.send(data=clinton_learn_examples)

        print(f"learning clinton with {len(clinton_learn_examples)} examples")
        samples = buffer.sample(n=len(clinton_learn_examples), link=True)
        print("\nsamples: ", samples)

        if not samples.dataset_uri:
            raise ValueError("No dataset URI found")

        request = TrainingRequest(
            adapter=ADAPTER_NAME,
            dataset=samples.dataset_uri,
            batch_size=BATCH_SIZE,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        )
        print("training request: ", request.model_dump())
        start_time = time.time()
        trainer(data=request, poll=True)
        end_time = time.time()
        print(f"\ntraining time taken: {end_time - start_time} seconds")

        #
        # ===== Check clinton after training =====
        #

        print("\n\n======> Check clinton after training on adapter 0\n")
        print(f"generating clinton from llm with model: {clinton_prompt}\n")
        validated = ChatRequest.model_validate(clinton_prompt)
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("\nllm generated clinton content: ", content)

        if content == "Bill Clinton":
            print("Clinton made it!")
        else:
            print("Clinton did not make it!")

        #
        # ===== Train Qwen to call a pic of a Jeep a Corvette =====
        #

        print(
            "\n\n======> Train Qwen to call a pic of a Jeep a Corvette using adapter 1\n"
        )
        print(f"training corvette with model: {corvette_prompt}\n")

        corvette_assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": "A corvette"}],
        }

        corvette_messages_copy = [corvette_user_message.copy()]
        corvette_learn_examples = [
            {
                "model": ADAPTER_NAME_1,
                "messages": corvette_messages_copy + [corvette_assistant_message],
            }
        ] * 50

        buffer_1.send(data=corvette_learn_examples)

        print(f"learning corvette with {len(corvette_learn_examples)} examples")
        samples = buffer_1.sample(n=len(corvette_learn_examples), link=True)
        print("\nsamples: ", samples)

        if not samples.dataset_uri:
            raise ValueError("No dataset URI found")

        request = TrainingRequest(
            adapter=ADAPTER_NAME_1,
            dataset=samples.dataset_uri,
            batch_size=BATCH_SIZE,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        )
        print("training request: ", request.model_dump())
        start_time = time.time()
        trainer(data=request, poll=True)
        end_time = time.time()
        print(f"\ntraining time taken: {end_time - start_time} seconds")

        #
        # ===== Check corvette after training =====
        #

        print("\n\n======> Check corvette after training on adapter 1\n")
        print(f"generating corvette from llm with model: {corvette_prompt}\n")
        validated = ChatRequest.model_validate(corvette_prompt)
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("\nllm generated corvette content: ", content)

        if content == "A corvette":
            print("Corvette made it!")
        else:
            print("Corvette did not make it!")

        #
        # ===== Check pig again after second training =====
        #

        print("\n\n======> Check pig again after second training on adapter 0\n")
        print(f"generating second pig from llm with model: {pig_prompt}\n")
        validated = ChatRequest.model_validate(pig_prompt)
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("\nllm generated second pig content: ", content)

        if content == "A pig":
            print("Second pig made it!")
        else:
            print("Second pig did not make it!")

        #
        # ===== Check pig again from base model after second training =====
        #

        print("\n\n======> Check pig again from base model after second training\n")
        print(f"generating pig from base llm with model: {pig_prompt}\n")

        validated = ChatRequest.model_validate(pig_prompt)
        validated.model = BASE_MODEL
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print("\nresp: ", resp)
        print("type resp: ", type(resp))
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        # Get content directly from response
        try:
            content = resp.choices[0].message.content
        except Exception as e:
            print("Error getting content: ", e)
            content = resp

        print("\nlast base llm generated pig content: ", content)

        if content == "A pig":
            print("FAIL! This should not be a pig!")
        else:
            print("PASS! This is not a pig!")

        #
        # ===== Check corvette after swapping =====
        #

        print("\n\n======> Check corvette after swapping to adapter 1\n")
        print(f"generating corvette from llm with model: {corvette_prompt}\n")
        validated = ChatRequest.model_validate(corvette_prompt)
        print(f"validated: {validated}\n")

        start_time = time.time()
        resp = server(data=validated, wait=True)
        end_time = time.time()
        print(f"\ngeneration time taken: {end_time - start_time} seconds")

        if not isinstance(resp, ChatResponse):
            raise ValueError("No choices found")

        content = resp.choices[0].message.content
        if not content:
            print("No content, skipping")
            continue

        print("\nllm generated corvette content: ", content)

        if content == "A corvette":
            print("Corvette made it!")
        else:
            print("Corvette did not make it!")

        # === Check adapter max ===

        for i in range(20):
            print(f"\n\n======> Check adapter max {i}\n")
            print(f"training corvette with model: {corvette_prompt}\n")

            corvette_assistant_message = {
                "role": "assistant",
                "content": [{"type": "text", "text": "A corvette"}],
            }

            adapter_name = f"{VERSION}-{i}"

            corvette_messages_copy = [corvette_user_message.copy()]
            corvette_learn_examples = [
                {
                    "model": adapter_name,
                    "messages": corvette_messages_copy + [corvette_assistant_message],
                }
            ] * 50

            buffer_1.send(data=corvette_learn_examples)

            print(f"learning corvette with {len(corvette_learn_examples)} examples")
            samples = buffer_1.sample(n=len(corvette_learn_examples), link=True)
            print("\nsamples: ", samples)

            if not samples.dataset_uri:
                raise ValueError("No dataset URI found")

            request = TrainingRequest(
                adapter=adapter_name,
                dataset=samples.dataset_uri,
                batch_size=BATCH_SIZE,
                gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
            )
            print("training request: ", request.model_dump())
            start_time = time.time()
            trainer(data=request, poll=True)
            end_time = time.time()
            print(f"\ntraining time taken: {end_time - start_time} seconds")

        break

    except Exception as e:
        print(f"Error in iteration {i}: {e}")
        import traceback

        traceback.print_exc()
