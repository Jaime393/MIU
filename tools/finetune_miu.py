#!/usr/bin/env python3
MIU Fine-tuning script using Unsloth + Llama-3.2-1B
# pip install unsloth datasets trl

MODEL = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"
HF_REPO = "Jaime393/miu-dataset"
OUTPUT_MODEL = "Jaime393/miu-llama-1b"

from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

def main():
    from unsloth import FastLanguageModel
    model, tokenizer = FastLanguageModel.from_pretrained(MODEL, max_seq_length=2048, load_in_4bit=True)
    model = FastLanguageModel.get_peft_model(model, r=16, target_modules=["q_proj","v_proj"], lora_alpha=16)
    ds = load_dataset(HF_REPO, split="train")
    trainer = SFTTrainer(model=model, tokenizer=tokenizer, train_dataset=ds, args=SFTConfig(output_dir="./miu_model", num_train_epochs=3, per_device_train_batch_size=2, fp16=True))
    trainer.train()
    model.save_pretrained_gguf("miu_gguf", tokenizer, quantization_method="q4_k_m")
    print("GGUF saved")

if __name__ == "__main__": main()