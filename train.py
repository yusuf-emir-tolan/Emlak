# -*- coding: utf-8 -*-

from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

model_name = "ytu-ce-cosmos/turkish-gpt2-large"  # Daha önce kullandýðýn model

# Tokenizer ve model yükle
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Pad token ekle (GPT-2'de yok)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

# Dataset oluþtur
def load_dataset(file_path):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128,
        overwrite_cache=True,
    )

train_dataset = load_dataset("train_data.txt")

# Data collator (Maskeli dil modelleme deðil, standart)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,
)

# Eðitim argümanlarý
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

# Trainer objesi
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Eðitimi baþlat
trainer.train()

# Eðitilen modeli kaydet
trainer.save_model("./emlak_gpt2_model")
tokenizer.save_pretrained("./emlak_gpt2_model")

print("Model egitimi tamamlandi ve kaydedildi.")
