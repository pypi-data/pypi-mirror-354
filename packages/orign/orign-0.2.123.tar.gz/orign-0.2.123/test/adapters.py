import gc
import os
import time

import torch
from peft import LoraConfig, PeftModel
from unsloth import FastVisionModel, is_bf16_supported
from unsloth_zoo.peft_utils import get_peft_regex  # For one-time capture if needed

# --- Global variable to store the initial target_modules pattern ---
# This will be captured after the first get_peft_model call
G_INITIAL_TARGET_MODULES_PATTERN = None

BASE_CKPT = "unsloth/Qwen2.5-VL-3B-Instruct"

print("Loading base model and tokenizer...")
base_model_instance, tok = FastVisionModel.from_pretrained(
    BASE_CKPT, dtype=torch.bfloat16, load_in_4bit=False, max_seq_length=32_768
)
print("Base model and tokenizer loaded.")

print("\nApplying initial PEFT setup with FastVisionModel.get_peft_model...")
plumbed_model: PeftModel = FastVisionModel.get_peft_model(
    base_model_instance,
    r=64,
    lora_alpha=128,
    lora_dropout=0.0,
    bias="none",
    finetune_vision_layers=True,
    finetune_language_layers=True,
    # target_modules is determined internally by Unsloth based on above flags
)
print(f"Type of model after get_peft_model: {type(plumbed_model)}")

# --- Capture the target_modules from the "default" adapter ---
if "default" in plumbed_model.peft_config:
    G_INITIAL_TARGET_MODULES_PATTERN = plumbed_model.peft_config[
        "default"
    ].target_modules
    print(f"Captured initial target_modules pattern from 'default' adapter's config.")

    print("Deleting 'default' adapter created by get_peft_model.")
    plumbed_model.delete_adapter("default")
else:
    print(
        "Warning: 'default' adapter not found. Attempting to generate target_modules pattern manually."
    )
    G_INITIAL_TARGET_MODULES_PATTERN = get_peft_regex(
        base_model_instance,
        finetune_vision_layers=True,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
    )
    print(f"Generated initial target_modules pattern (fallback).")

if G_INITIAL_TARGET_MODULES_PATTERN is None:
    raise RuntimeError("Could not determine initial target_modules pattern. Aborting.")

plumbed_model.active_adapter = None
print(
    f"Initial target_modules pattern to be reused: '{str(G_INITIAL_TARGET_MODULES_PATTERN)[:200]}...'"
)

import os

from trl import SFTConfig, SFTTrainer
from unsloth.trainer import UnslothVisionDataCollator

ADIR = "./adapters"
os.makedirs(ADIR, exist_ok=True)


def add_or_load_adapter_for_model(
    model: PeftModel, adapter_name: str, resume_training: bool
):
    global G_INITIAL_TARGET_MODULES_PATTERN
    print(
        f"\n[Adapter Management] Called for adapter: '{adapter_name}', resume: {resume_training}"
    )

    # This is the base folder for the adapter (e.g., ./adapters/adapter_A)
    adapter_base_folder = os.path.join(ADIR, adapter_name)
    os.makedirs(adapter_base_folder, exist_ok=True)  # Ensure base folder exists

    # Based on logs (ls adapters/adapter_A/adapter_A/), PEFT saves into a nested subdirectory
    # if save_pretrained is called with a path like "./adapters/adapter_A" and adapter name "adapter_A".
    # So, the actual files (adapter_config.json, etc.) are expected in this nested path.
    path_containing_adapter_files = os.path.join(adapter_base_folder, adapter_name)

    if adapter_name not in model.peft_config:
        print(
            f"[Adapter Management] Adapter '{adapter_name}' not found in peft_config. Adding new adapter configuration."
        )

        new_lora_config = LoraConfig(
            r=64,
            lora_alpha=128,
            lora_dropout=1e-3,
            bias="none",
            target_modules=G_INITIAL_TARGET_MODULES_PATTERN,
        )
        try:
            model.add_adapter(adapter_name=adapter_name, peft_config=new_lora_config)
            print(
                f"[Adapter Management] Adapter '{adapter_name}' added with new config."
            )
        except Exception as e:
            print(
                f"[Adapter Management] Error during model.add_adapter for '{adapter_name}': {e}"
            )
            raise
    else:
        print(
            f"[Adapter Management] Adapter '{adapter_name}' already exists in peft_config."
        )

    if resume_training:
        print(
            f"[Adapter Management] Attempting to load weights for adapter '{adapter_name}'."
        )
        print(
            f"[Adapter Management] Expected adapter files location: {path_containing_adapter_files}"
        )
        if os.path.isdir(path_containing_adapter_files):
            print(
                f"[Adapter Management] Contents of '{path_containing_adapter_files}': {os.listdir(path_containing_adapter_files)}"
            )
            try:
                # Load from the path where adapter_config.json and weights are actually located
                model.load_adapter(
                    path_containing_adapter_files, adapter_name, is_trainable=True
                )
                print(
                    f"[Adapter Management] Successfully loaded weights for adapter '{adapter_name}' from '{path_containing_adapter_files}'."
                )
            except Exception as e:
                print(
                    f"[Adapter Management] Error loading adapter weights for '{adapter_name}' from '{path_containing_adapter_files}': {e}"
                )
        else:
            print(
                f"[Adapter Management] Path '{path_containing_adapter_files}' does not exist or is not a directory. Cannot load weights."
            )

    model.set_adapter(adapter_name)
    print(f"[Adapter Management] Active adapter(s) set to: '{model.active_adapters}'")
    # The folder returned is the base folder where the nested adapter specific folder is.
    # For saving, we'll save to adapter_base_folder, and PEFT will create the nested structure if it does so.
    return adapter_base_folder


def drop_adapter_from_model(model: PeftModel, adapter_name_to_drop: str):
    print(
        f"\n[Adapter Management] Attempting to drop adapter: '{adapter_name_to_drop}'"
    )
    print(
        f"[Adapter Management] Current peft_config keys before deleting: {list(model.peft_config.keys())}"
    )
    print(
        f"[Adapter Management] Currently active adapters before deleting: {model.active_adapters}"
    )

    if adapter_name_to_drop in model.peft_config:
        try:
            print(
                f"[Adapter Management] Calling model.delete_adapter('{adapter_name_to_drop}')..."
            )
            model.delete_adapter(adapter_name_to_drop)
            print(
                f"[Adapter Management] Adapter '{adapter_name_to_drop}' deleted successfully from peft_config."
            )
        except Exception as e:
            print(
                f"[Adapter Management] Error during model.delete_adapter('{adapter_name_to_drop}'): {e}"
            )
    else:
        print(
            f"[Adapter Management] Adapter '{adapter_name_to_drop}' not found in peft_config. Cannot delete."
        )

    if not model.active_adapters:
        model.active_adapter = None
        print(
            f"[Adapter Management] No active adapters remain. Set model.active_adapter to None."
        )
    else:
        print(
            f"[Adapter Management] Active adapters after drop attempt: {model.active_adapters}"
        )

    torch.cuda.empty_cache()
    gc.collect()
    print(f"[Adapter Management] Finished dropping adapter '{adapter_name_to_drop}'.\n")


def train_lora_adapter(
    adapter_name_to_train,
    training_dataset,
    num_epochs=1,
    resume_from_saved_state=False,
    checkpoint_path=None,
):
    global plumbed_model, tok

    print(
        f"\n--- Starting train_lora_adapter for adapter: '{adapter_name_to_train}' (Epochs: {num_epochs}, Resume: {resume_from_saved_state}) ---"
    )

    # add_or_load_adapter_for_model now returns the base save folder (e.g., ./adapters/adapter_A)
    adapter_base_save_folder = add_or_load_adapter_for_model(
        plumbed_model,
        adapter_name_to_train,
        resume_from_saved_state or bool(checkpoint_path),
    )
    print(
        f"Adapter base save folder for '{adapter_name_to_train}': {adapter_base_save_folder}"
    )

    print("\nPreparing model for training with FastVisionModel.for_training...")
    model_ready_for_training = FastVisionModel.for_training(plumbed_model)
    print("Model prepared for training.")

    print("\nModel's trainable parameters (on instance passed to SFTTrainer):")
    try:
        model_ready_for_training.print_trainable_parameters()
    except AttributeError:
        total_params = sum(p.numel() for p in model_ready_for_training.parameters())
        trainable_params = sum(
            p.numel() for p in model_ready_for_training.parameters() if p.requires_grad
        )
        print(
            f"trainable params: {trainable_params:,} || all params: {total_params:,} || trainable%: {100 * trainable_params / total_params:.4f}"
        )

    initial_learning_rate = 5e-5
    print(f"Using initial learning_rate for SFTTrainer: {initial_learning_rate}")

    sft_config_args = SFTConfig(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        num_train_epochs=num_epochs,
        learning_rate=initial_learning_rate,
        optim="adamw_torch",
        fp16=not is_bf16_supported(),
        bf16=is_bf16_supported(),
        save_strategy="steps",
        save_steps=2,
        output_dir=f"./runs/{adapter_name_to_train}",  # SFTTrainer checkpoints go here
        logging_steps=1,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model_ready_for_training,
        tokenizer=tok,
        data_collator=UnslothVisionDataCollator(
            model_ready_for_training, tok, resize="max"
        ),
        train_dataset=training_dataset,
        args=sft_config_args,
    )

    # For SFTTrainer's resume_from_checkpoint:
    # If checkpoint_path is explicitly given, use it.
    # Else, if resume_from_saved_state is True, pass True to trainer.train() to load latest from output_dir.
    # Otherwise, no resume.
    sft_trainer_resume_arg = None
    if checkpoint_path:
        sft_trainer_resume_arg = checkpoint_path
        print(
            f"SFTTrainer will attempt to resume from EXPLICIT checkpoint path: '{sft_trainer_resume_arg}'"
        )
    elif resume_from_saved_state:
        sft_trainer_resume_arg = (
            True  # Let Trainer find the latest checkpoint in output_dir
        )
        print(
            f"SFTTrainer will attempt to resume from the latest checkpoint in its output_dir: {sft_config_args.output_dir}"
        )
    else:
        print(
            "SFTTrainer training from scratch (no SFTTrainer checkpoint specified or found for resume)."
        )

    # Check if the directory for SFTTrainer resume exists if a path was constructed (not True)
    if isinstance(sft_trainer_resume_arg, str) and not os.path.isdir(
        sft_trainer_resume_arg
    ):
        print(
            f"Warning: SFTTrainer resume path '{sft_trainer_resume_arg}' not found. Training from scratch."
        )
        sft_trainer_resume_arg = None  # Fallback to no resume

    print("\nStarting SFTTrainer training...")
    trainer.train(resume_from_checkpoint=sft_trainer_resume_arg)
    print("SFTTrainer training finished.")

    # Save adapter weights to the base folder. PEFT might create a nested folder.
    # Example: if adapter_base_save_folder is "./adapters/adapter_A", PEFT saves to "./adapters/adapter_A/adapter_A/"
    # This matches the loading logic.
    print(
        f"\nSaving adapter weights for '{adapter_name_to_train}' to base folder: {adapter_base_save_folder}"
    )
    model_ready_for_training.save_pretrained(adapter_base_save_folder)
    print("Adapter weights saved.")

    drop_adapter_from_model(plumbed_model, adapter_name_to_train)

    del trainer, model_ready_for_training
    torch.cuda.empty_cache()
    gc.collect()
    print(
        f"--- train_lora_adapter for adapter: '{adapter_name_to_train}' completed ---\n"
    )


# --- Dataset Loading (User's Preferred Version) ---
import json
import time

import requests
from chatmux import oai_to_unsloth

print("\nLoading and converting dataset using user's original method...")
dataset_url = "https://nebulous-rs.s3.us-east-1.amazonaws.com/samples/pbarker/buffers/1yeW2wrRgQh3kuPMToXMn2/1745951330990/sample-hOaBzUeB.jsonl"
dataset_file = "downloaded_user_dataset.jsonl"

if not os.path.exists(dataset_file):
    print(f"Downloading dataset from {dataset_url} to {dataset_file}...")
    response = requests.get(dataset_url)
    response.raise_for_status()
    with open(dataset_file, "w", encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))
    print("Dataset downloaded.")
else:
    print(f"Dataset already exists at {dataset_file}. Loading from local file.")

with open(dataset_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Processing {len(lines)} lines from the dataset...")
time_start_convert = time.time()
converted_dataset = []
for idx, line_str in enumerate(lines):
    line_str_stripped = line_str.strip()
    if line_str_stripped:
        try:
            json_loaded_line = json.loads(line_str_stripped)
            converted_sample = oai_to_unsloth(json_loaded_line)
            if not (
                isinstance(converted_sample, dict) and "messages" in converted_sample
            ):
                print(
                    f"Warning: oai_to_unsloth output for line {idx} might be malformed: {converted_sample}"
                )
            converted_dataset.append(converted_sample)
        except json.JSONDecodeError as e:
            print(
                f"Error decoding JSON at line {idx}: '{line_str_stripped[:100]}...' - {e}"
            )
        except Exception as e:
            print(f"Error processing line {idx} ('{line_str_stripped[:100]}...'): {e}")
            continue

print(f"Time to convert dataset: {time.time() - time_start_convert:.2f} seconds")

if not converted_dataset:
    print(
        "Dataset is empty after conversion. Please check dataset file and oai_to_unsloth function. Exiting."
    )
    exit()

print("\nConverted dataset example [0]:")
if converted_dataset:
    example_to_print = converted_dataset[0]
    if isinstance(example_to_print, dict) and "messages" in example_to_print:
        print("{'messages': [")
        for msg_idx, msg in enumerate(example_to_print["messages"]):
            print(f"  {{'role': '{msg.get('role', 'N/A')}', 'content': [")
            if isinstance(msg.get("content"), list):
                for content_idx, item in enumerate(msg["content"]):
                    if item.get("type") == "image":
                        img_obj = item.get("image")
                        img_repr = (
                            f"<PIL.Image object at {hex(id(img_obj))}>"
                            if img_obj is not None
                            else "None"
                        )
                        print(f"    {{'type': 'image', 'image': {img_repr}}}", end="")
                    else:
                        print(f"    {item}", end="")
                    if content_idx < len(msg["content"]) - 1:
                        print(",")
                    else:
                        print()
            else:
                print(f"    {msg.get('content')}")
            print("  ]", end="")
            if msg_idx < len(example_to_print["messages"]) - 1:
                print(",")
            else:
                print()
        print("]}")
    else:
        print(str(example_to_print)[:500] + "...")
else:
    print("Converted dataset is empty.")

print("Number of samples in dataset:", len(converted_dataset))

print(
    "\nChecking trainable tensors on `plumbed_model` (before first train_lora_adapter call):"
)
trainable_tensors_before = sum(
    p.numel() for p in plumbed_model.parameters() if p.requires_grad
)
print(f"Trainable parameters in `plumbed_model`: {trainable_tensors_before:,}")


# --- Start Multi-Adapter Training Sequence ---
print("\n--- Starting Multi-Adapter Training Sequence ---")

# 1. Train Adapter A (initial)
start_time = time.time()
train_lora_adapter(
    adapter_name_to_train="adapter_A",
    training_dataset=converted_dataset,
    num_epochs=1,
    resume_from_saved_state=False,
)
end_time = time.time()
print(f"trained in {end_time - start_time} seconds")

# 2. Train Adapter B (initial)
train_lora_adapter(
    adapter_name_to_train="adapter_B",
    training_dataset=converted_dataset,
    num_epochs=1,
    resume_from_saved_state=False,
)

# 3. Train Adapter C (initial)
train_lora_adapter(
    adapter_name_to_train="adapter_C",
    training_dataset=converted_dataset,
    num_epochs=1,
    resume_from_saved_state=False,
)

# 4. Resume training Adapter A
print("\n--- Attempting to RESUME training for adapter_A (another epoch) ---")
start_time = time.time()
train_lora_adapter(
    adapter_name_to_train="adapter_A",
    training_dataset=converted_dataset,
    num_epochs=2,
    resume_from_saved_state=True,
)
end_time = time.time()
print(f"trained in {end_time - start_time} seconds")

# 5. Resume training Adapter B
print("\n--- Attempting to RESUME training for adapter_B (another epoch) ---")
train_lora_adapter(
    adapter_name_to_train="adapter_B",
    training_dataset=converted_dataset,
    num_epochs=2,
    resume_from_saved_state=True,
)

print("\n--- Multi-Adapter Training Sequence Completed ---")
print("\nMain script execution finished.")
