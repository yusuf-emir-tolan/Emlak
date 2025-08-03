# -*- coding: utf-8 -*-
import gradio as gr
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_path = "./emlak_gpt2_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token

def generate(prompt, max_length):
    input_ids = tokenizer.encode(prompt, return_tensors="pt", truncation=True)
    
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=10,  # 10 farklı ilan
        temperature=0.9,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True  # sampling açık
    )

    ilanlar = []
    for output in outputs:
        text = tokenizer.decode(output, skip_special_tokens=True)
        ilanlar.append(text.strip())

    return "\n\n---\n\n".join(ilanlar)


demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Başlangıç metni", placeholder="Örn: İstanbul Kadıköy'de 3+1 geniş daire...", lines=2),
        gr.Slider(50, 500, step=10, value=200, label="Maksimum Uzunluk")
    ],
    outputs=gr.Textbox(label="Üretilen İlanlar", lines=15),
    title="🏘️ EmlakGPT - İlan Üretici",
    description="",
    theme="default"
)

if __name__ == "__main__":
    demo.launch()

