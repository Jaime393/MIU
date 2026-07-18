Aquí tienes un script de fine-tuning para Llama-3.2-1B-Instruct utilizando el dataset Jaime393/miu-dataset en formato Alpaca, con 3 epochs de SFT y exportación a GGUF q4_k_m:

```python
from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from peft import LoraConfig
import os

# Configuración inicial
max_seq_length = 2048  # Ajusta según tus necesidades
dtype = None  # None para auto-detección, float16 o bfloat16 para especificar
load_in_4bit = True  # Usar 4bit para reducir el uso de memoria

# Cargar el modelo
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="meta-llama/Llama-3.2-1B-Instruct",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# Configuración de LoRA
lora_config = LoraConfig(
    r=16,  # Dimensión de la matriz LoRA
    lora_alpha=32,  # Alpha de LoRA
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],  # Capas objetivo
    lora_dropout=0.05,  # Dropout de LoRA
    bias="none",  # No ajustar los sesgos
    task_type="CAUSAL_LM",  # Tipo de tarea
)

# Aplicar LoRA al modelo
model = FastLanguageModel.get_peft_model(
    model,
    lora_config=lora_config,
)

# Cargar el dataset
dataset = load_dataset("Jaime393/miu-dataset", split="train")

# Formatear el dataset en formato Alpaca
def formatting_prompts_func(examples):
    outputs = []
    for i in range(len(examples["instruction"])):
        text = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{examples['instruction'][i]}\n\n### Input:\n{examples['input'][i]}\n\n### Response:\n{examples['output'][i]}"
        outputs.append(text)
    return outputs

# Aplicar el formateo al dataset
dataset = dataset.map(formatting_prompts_func, batched=True)

# Configuración del entrenamiento
training_args = TrainingArguments(
    per_device_train_batch_size=2,  # Tamaño del batch por dispositivo
    gradient_accumulation_steps=4,  # Pasos de acumulación de gradiente
    warmup_steps=5,  # Pasos de calentamiento
    max_steps=60,  # Pasos máximos (3 epochs con 44 registros y batch_size=2)
    learning_rate=2e-4,  # Tasa de aprendizaje
    fp16=not torch.cuda.is_bf16_supported(),  # Usar fp16 si no se soporta bf16
    bf16=torch.cuda.is_bf16_supported(),  # Usar bf16 si se soporta
    logging_steps=1,  # Pasos de registro
    optim="adamw_8bit",  # Optimizador
    weight_decay=0.01,  # Decaimiento del peso
    lr_scheduler_type="linear",  # Tipo de programador de tasa de aprendizaje
    seed=42,  # Semilla para reproducibilidad
    output_dir="outputs",  # Directorio de salida
)

# Configuración del entrenador
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,  # Procesos para el dataset
    packing=False,  # No empaquetar los ejemplos
    args=training_args,
)

# Entrenar el modelo
trainer.train()

# Guardar el modelo
model.save_pretrained("miu-llama-1b")  # Guarda el modelo en el directorio especificado

# Exportar a GGUF q4_k_m
model.push_to_hub_gguf(
    "Jaime393/miu-llama-1b",  # Nombre del repositorio en HuggingFace
    tokenizer,
    quantization_method="q4_k_m",  # Método de cuantización
    max_shard_size="10GB",  # Tamaño máximo del fragmento
)

print("Entrenamiento completado y modelo exportado a GGUF q4_k_m.")
```

### Notas importantes:
1. **Requisitos**: Asegúrate de tener instalados los paquetes necesarios (`unsloth`, `torch`, `datasets`, `trl`, `transformers`, `peft`, `huggingface_hub`).
2. **Hardware**: Este script está diseñado para ser ejecutado en un entorno con GPU. Ajusta `per_device_train_batch_size` y `gradient_accumulation_steps` según la capacidad de tu GPU.
3. **Dataset**: El dataset se carga directamente desde HuggingFace. Asegúrate de que el formato del dataset coincida con el esperado (instruction, input, output).
4. **Exportación**: El modelo se exporta a GGUF q4_k_m y se sube a HuggingFace. Asegúrate de tener acceso y permisos para subir modelos a tu cuenta de HuggingFace.
5. **Epochs**: Con 44 registros y un batch_size de 2, 60 pasos equivalen a 3 epochs (60 pasos * 2 registros/batch / 44 registros = 3 epochs).

Ajusta los parámetros según tus necesidades específicas y recursos disponibles.