# -*- coding: utf-8 -*-
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)

page_count = 15
veriler = []

try:
    for page in range(1, page_count + 1):
        url = f"https://www.sahibinden.com/satilik?page={page}"
        print(f"\nSayfa {page} indiriliyor: {url}")
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchResultsItem"))
        )
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all("tr", class_="searchResultsItem")
        print(f"  {len(items)} ilan bulundu.")

        for item in items:
            title_td = item.find("td", class_="searchResultsTitleValue")
            title = title_td.find("a", class_="classifiedTitle").text.strip() if title_td else "YOK"

            price_td = item.find("td", class_="searchResultsPriceValue")
            price = price_td.get_text(strip=True).replace("TL", "").replace(".", "").replace(",", ".") if price_td else "0"

            location_td = item.find("td", class_="searchResultsLocationValue")
            location = location_td.get_text(separator=" ", strip=True) if location_td else "YOK"

            veriler.append([title, price, location])
        
        time.sleep(2)

finally:
    print("\nislem tamamlandi, tarayici kapatiliyor...")
    try:
        driver.quit()
    except:
        pass

with open("emlak_verisi.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Baslik", "Fiyat", "Konum"])
    writer.writerows(veriler)

print(f"\nToplam ilan sayisi: {len(veriler)}")
