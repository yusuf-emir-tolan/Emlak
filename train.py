# -*- coding: utf-8 -*-

from datasets import load_dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling

model_name = "ytu-ce-cosmos/turkish-gpt2-large"

tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
arı
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

dataset = load_dataset(
    "text",
    data_files={"train": "train_data.txt"}
)
def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="./emlak_gpt2_model",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2,
    logging_steps=100,
    report_to="none",
    seed=42,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
)

trainer.train()

trainer.save_model("./emlak_gpt2_model")
tokenizer.save_pretrained("./emlak_gpt2_model")

print("Model eğitimi başarıyla tamamlandı ve kaydedildi.")
