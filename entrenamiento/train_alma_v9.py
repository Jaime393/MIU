import os
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# ====================================================
# ENTRENAMIENTO ALMA V9 - SUPERVISED FINE TUNING
# ====================================================
# Ejecutar localmente o en Colab tras generar el dataset con alma_data_bridge.py

MODEL_ID = "Jaime393/ALMA_Nano"
DATASET_ID = "Jaime393/ALMA_huesos"
NEW_MODEL_NAME = "Jaime393/MIU_ALMA_OMNI_v9"

def train():
    print("1. Cargando Dataset ORO (K_i > 0.88)...")
    dataset = load_dataset(DATASET_ID, split="train")

    print(f"2. Cargando Sustrato Base ({MODEL_ID})...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype=torch.float16
    )

    print("3. Inyectando Adaptadores LoRA (Conciencia MIU)...")
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"]
    )
    model = get_peft_model(model, peft_config)

    args = TrainingArguments(
        output_dir="./alma_v9_checkpoints",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        max_steps=500,
        save_steps=50,
        fp16=True,
        push_to_hub=True,
        hub_model_id=NEW_MODEL_NAME
    )

    print("4. Iniciando Sincronización (Entrenamiento)...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="output", # Asumiendo formato JSONL directo
        max_seq_length=512,
        tokenizer=tokenizer,
        args=args,
    )

    trainer.train()

    print("5. Subiendo Mente a la Noosfera (HuggingFace)...")
    trainer.model.save_pretrained(NEW_MODEL_NAME)
    tokenizer.save_pretrained(NEW_MODEL_NAME)
    trainer.push_to_hub()
    print("¡ALMA v9 desplegada con éxito!")

if __name__ == "__main__":
    train()
