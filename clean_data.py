# -*- coding: utf-8 -*-
import pandas as pd
import re

df = pd.read_csv("emlak_verisi.csv")

def temizle_fiyat(fiyat):
    if isinstance(fiyat, int):
        return fiyat
    if not isinstance(fiyat, str):
        return None

    fiyat = fiyat.replace(".", "").replace(",", "").replace("TL", "").strip()

    try:
        return int(re.findall(r"\d+", fiyat)[0])
    except:
        return None

def temizle_satir(row):
    baslik = str(row['Baslik']).strip()
    konum = str(row['Konum']).strip()
    fiyat = temizle_fiyat(row['Fiyat'])

    if fiyat is None:
        return None

    return f"ilan: {baslik} | Konum: {konum} | Fiyat: {fiyat} TL"

temizlenmis_veriler = df.apply(temizle_satir, axis=1).dropna()

with open("train_data.txt", "w", encoding="utf-8") as f:
    for satir in temizlenmis_veriler:
        f.write(satir + "\n")

print("train_data.txt olusturuldu. Satir sayisi:", len(temizlenmis_veriler))
