# -*- coding: utf-8 -*-
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# Model ve tokenizer adı
model_name = "ytu-ce-cosmos/turkish-gpt2-large"

# Tokenizer ve model yükleme
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Pad token olarak eos token'ı kullanıyoruz

model = GPT2LMHeadModel.from_pretrained(model_name)
model.config.pad_token_id = tokenizer.eos_token_id  # Modelde pad_token_id ayarla

# Örnek veri (Sen kendi veri setinle değiştirebilirsin)
texts = [
    "Merhaba, nasılsın?",
    "Bu bir örnek cümledir.",
    "Türkçe GPT-2 modeli ile çalışıyoruz.",
    "Transformers kütüphanesi çok güçlü.",
    "Modelimizi eğiteceğiz."
]

# Dataset oluşturma
dataset = {"text": texts}
train_dataset = Dataset.from_dict(dataset)

# Tokenize ve 'labels' ekle
def tokenize_function(examples):
    tokenized = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=64,
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

train_dataset = train_dataset.map(tokenize_function, batched=True)
train_dataset = train_dataset.remove_columns(["text"])
train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Eğitim argümanları
training_args = TrainingArguments(
    output_dir="./emlak_gpt2_model",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    logging_steps=10,
    save_steps=10,
    save_total_limit=2,
    prediction_loss_only=True,
    report_to="none",  # Loglama servisi kullanmıyorsan
)

# Trainer oluştur
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Eğitimi başlat
trainer.train()
