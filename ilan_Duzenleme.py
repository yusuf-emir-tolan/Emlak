# -*- coding: utf-8 -*-
import pandas as pd
import re

# İlan verilerin
data = [
    {'title': "MESUT EMLAK'TAN 50.YIL DA 4+1 BAĞIMSIZ MUTFAK SATILIK LÜKS DAİRE", 'price': "8.950.000 TL", 'location': "Mersin Yenişehir"},
    {'title': "HASANAĞA CİVARINDA 20.000 TL KİRA GETİRİLİ LÜKS 1+1 DAİRE", 'price': "1.240.000 TL", 'location': "İzmir Buca"},
]

# Temizleme fonksiyonu
def clean_price(text):
    if "TL" in text:
        text = text.replace("TL", "").replace(".", "").replace(",", "").strip()
        return int(text)
    return None

# Temiz format için liste
lines = []
for ilan in data:
    title = ilan['title']
    location = ilan['location']
    price = clean_price(ilan['price'])

    if title and location and price:
        line = f"İlan: {title}\nKonum: {location}\nFiyat: {price} TL\n---"
        lines.append(line)

# Eğitim dosyasını yaz
with open("emlak_data.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("✅ Veriler 'emlak_data.txt' dosyasına yazıldı.")

