# -*- coding: utf-8 -*-
"""Support Agent Chatbot .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10z8jQiQVV5yLg3-n73Z_es980pkcbHl4
"""

# locale -k LC_ALL=en_US.UTF-8
pip install -q accelerate==0.21.0 peft==0.4.0 transformers==4.31.0 bitsandbytes==0.40.2 trl==0.4.7
pip install datasets

import os
import torch
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers import BitsAndBytesConfig, TrainingArguments, Trainer
from transformers import logging, HfArgumentParser, PushToHubCallback
from peft import LoraConfig, PeftModel
from transformers import TrainingArguments, Trainer
from trl import SFTTrainer
import pandas as pd

# The model that you want to train from the Hugging Face hub
# model_name = "meta-llama/Llama-2-7b-chat-hf"
# model_name = "facebook/bart-base"
model_name= "TinyLlama/TinyLlama_v1.1"

# The instruction dataset to use
# dataset_name = "mlabonne/guanaco-llama2-1k"
# dataset_name = "RBI_final_data-Sheet1.csv"
dataset_name = "hugging_face_banking.csv"
dataset_name = "WEB_DATA_FINAL.csv"


# Fine-tuned model name
new_model = "tinyLlama-2-7b-chat-finetuned-bankingdata"
# new_model = "facebook-bart-base-finetune"

# QLoRA parameters
# LoRA attention dimension
lora_r = 64

# Alpha parameter for LoRA scaling
lora_alpha = 16

# Dropout probability for LoRA layers
lora_dropout = 0.1

# bitsandbytes parameters
# Activate 4-bit precision base model loading
use_4bit = True

# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16" #USE THIS IF NOT WORKING WITH 4BIT PRECISION

# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4" #TAKES LESS SPACE FOR IMPORTANT INFORMATION

# Activate nested quantization for 4-bit base models (double quantization)
use_nested_quant = False #DECIDES IF THE MODEL NEED MORE COMPRESSION TO SAVE SPACE OR NOT

# TrainingArguments parameters
# Output directory where the model predictions and checkpoints will be stored
output_dir = "./results"

# Number of training epochs
# num_train_epochs = 10

# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = False
bf16 = False

# Batch size per GPU for training
per_device_train_batch_size = 1

# Batch size per GPU for evaluation
per_device_eval_batch_size = 5

# Number of update steps to accumulate the gradients for
gradient_accumulation_steps = 1

# Enable gradient checkpointing
gradient_checkpointing = True

# Maximum gradient normal (gradient clipping)
max_grad_norm = 0.3

# Initial learning rate (AdamW optimizer)
learning_rate = 2e-4

# Weight decay to apply to all layers except bias/LayerNorm weights
weight_decay = 0.001

# Optimizer to use
optim = "paged_adamw_32bit"

# Learning rate schedule
lr_scheduler_type = "cosine"

# Number of training steps (overrides num_train_epochs)
max_steps = -1

# Ratio of steps for a linear warmup (from 0 to learning rate)
warmup_ratio = 0.03

# Group sequences into batches with same length
# Saves memory and speeds up training considerably
group_by_length = True

# Save checkpoint every X updates steps
save_steps = 0

# Log every X updates steps
logging_steps = 25

################################################################################
# SFT parameters
################################################################################

# Maximum sequence length to use
max_seq_length = None

# Pack multiple short examples in the same input sequence to increase efficiency
packing = False

# Load the entire model on the GPU 0
device_map = {"": 0}

# !export LC_ALL=C.UTF-8


from huggingface_hub import login
import os
key = os.environ.get("tonken")  # Access the token from secrets
login(token=key)

from datasets import Dataset
import pandas as pd
# # Load your CSV data
dataset = pd.read_csv("WEB_DATA_FINAL.csv")
# # Assuming your text data is in a column named "text"
# user_queries = dataset["USER_QUERIES"].tolist()
# web_responses = dataset["WEB_RESPONSES"].tolist()

# Convert DataFrame to Hugging Face Dataset
dataset = Dataset.from_pandas(dataset)

# for direct use of huggingFace dataset
# dataset = load_dataset(dataset_name, split="train")

# Load tokenizer and model with QLoRA configuration
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

bnb_config = BitsAndBytesConfig(
    # load_in_4bit=use_4bit,
    load_in_4bit=False,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)

# Check GPU compatibility with bfloat16
if compute_dtype == torch.float16 and use_4bit:
    major, _ = torch.cuda.get_device_capability()
    if major >= 8:
        print("=" * 80)
        print("Your GPU supports bfloat16: accelerate training with bf16=True")
        print("=" * 80)

# Load base model

# ====for tinyllama/tinyllama-1.1b-chat-v1.0====
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map=device_map
)

model.config.use_cache = False
model.config.pretraining_tp = 1

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

# Load LoRA configuration
peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
)

# Set training parameters
training_arguments = TrainingArguments(
    output_dir=output_dir,
    # num_train_epochs=num_train_epochs, #5 epochs
    num_train_epochs=1,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=save_steps,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=fp16,
    bf16=bf16,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=group_by_length,
    lr_scheduler_type=lr_scheduler_type,
    report_to="tensorboard"
)

# Set supervised fine-tuning parameters
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    # dataset_text_field="text", #for hugging_face_banking.csv
    # dataset_text_field="Text", #for RBI_final_data-sheet1.csv
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=packing,
)

# Train model
trainer.train()

# Save trained model
trainer.model.save_pretrained(new_model)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir results/runs

def chat_with_bot(prompt):

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
    result = pipe(f"<s>[INST] {prompt} [/INST]", max_length=200, pad_token_id=tokenizer.eos_token_id, num_return_sequences=1)

    generated_text = result[0]['generated_text']
    response = generated_text.split('[/INST]')[-1].strip()

    bot_tag = f"\033[1;34mBOT:\033[0m"  # Bold blue text
    user_tag = f"\033[1;31mUSER:\033[0m"  # Bold red text
    border = "=" * 200

    print(f"\n{border}\n")
    print(f"{user_tag} {prompt}")
    print(f"{bot_tag} {response}")
    print(f"{border}\n")

prompt = "can you predict stock prices?"
chat_with_bot(prompt)

from IPython.display import display, HTML
import ipywidgets as widgets

# Define the chatbot function
def chat_with_bot(prompt):
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
    result = pipe(f"<s>[INST] {prompt} [/INST]", max_length=200, pad_token_id=tokenizer.eos_token_id, num_return_sequences=1)
    generated_text = result[0]['generated_text']
    response = generated_text.split('[/INST]')[-1].strip()

    bot_tag = f"\033[1;34mBOT:\033[0m"  # Bold blue text
    user_tag = f"\033[1;31mUSER:\033[0m"  # Bold red text
    border = "=" * 200

    display(HTML(f"""
    <div style="white-space: pre-wrap;">
    <p style="color: red; font-weight: bold;">USER: {prompt}</p>
    <p style="color: blue; font-weight: bold;">BOT: {response}</p>
    <hr style="border: solid 1px black;">
    </div>
    """))

# Define the input widgets
input_prompt = widgets.Text(
    value='',
    placeholder='Type your message here...',
    description='Message:',
    disabled=False
)

send_button = widgets.Button(
    description='Send',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Send message',
    icon='check'
)

output = widgets.Output()

# Define the event handler for the button click
def on_button_clicked(b):
    with output:
        output.clear_output()
        chat_with_bot(input_prompt.value)
        input_prompt.value = ''

send_button.on_click(on_button_clicked)

# Display the input form
display(input_prompt, send_button, output)

"""### **push the fine tuned model to hugging face **"""

# import locale
# locale.getpreferredencoding = lambda: "UTF-8"

# # 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

# # model.push_to_hub(new_model)
# # tokenizer.push_to_hub("entbappy/Llama-2-7b-chat-finetune",check_pr=True)

# !huggingface-cli login

# model.push_to_hub("new_model", check_pr=True)

# tokenizer.push_to_hub("siddhant2610/Llama-2-7b-chat-finetuned_banking",check_pr=True)

# # repoName = siddhant2610/Llama-2-7b-chat-finetuned_banking

# from transformers import AutoModel

# model = AutoModel.from_pretrained("siddhant2610/Llama-2-7b-chat-finetuned_banking")