```python
import os
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel
from huggingface_hub import login

# Constants
MODEL_NAME = "unsloth/llama-3-8b-Instruct-bnb-4bit"
DATASET_NAME = "Jaime393/miu-dataset"
OUTPUT_MODEL_NAME = "Jaime393/miu-llama-1b"
HF_TOKEN = os.getenv("HF_TOKEN")

# Login to Hugging Face
login(token=HF_TOKEN)

# Load dataset
dataset = load_dataset(DATASET_NAME)

# Format dataset for Alpaca
def format_dataset(example):
    return {
        "text": f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
    }

dataset = dataset.map(format_dataset)

# Load model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=2048,
    dtype=torch.float16,
    load_in_4bit=True,
)

# Training arguments
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=5,
    max_steps=100,
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=42,
    output_dir="outputs",
)

# SFT Trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    dataset_text_field="text",
    max_seq_length=2048,
    args=training_args,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained(OUTPUT_MODEL_NAME)
tokenizer.save_pretrained(OUTPUT_MODEL_NAME)

# Export to GGUF format
model.push_to_hub_gguf(
    OUTPUT_MODEL_NAME,
    tokenizer,
    quantization_method="q4_k_m",
    token=HF_TOKEN,
)

# Upload to Hugging Face Hub
model.push_to_hub(OUTPUT_MODEL_NAME, token=HF_TOKEN)
tokenizer.push_to_hub(OUTPUT_MODEL_NAME, token=HF_TOKEN)
```