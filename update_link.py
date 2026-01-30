import cloudscraper
import re
import os

def get_atv_link():
    # Daha güçlü bir tarayıcı taklidi
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    # Kaynak listesini genişlettik ve daha stabil olanları başa aldık
    urls = [
        "https://www.canlitv.me/atv-canli-izle-1",
        "https://m.canlitv.direct/atv-canli-yayin-izle",
        "https://canlitv.center/atv-canli-yayin"
    ]
    
    # Daha agresif bir Regex: tırnak içindeki her türlü m3u8 yapısını yakalar
    pattern = r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']'

    print("--- ATV Link Avcısı Başlatıldı ---")

    for url in urls:
        try:
            print(f"Kaynak taranıyor: {url}")
            response = scraper.get(url, timeout=20)
            
            if response.status_code == 200:
                # Tüm eşleşmeleri bul
                matches = re.findall(pattern, response.text)
                for link in matches:
                    # Kaçış karakterlerini (\/) temizle
                    clean_link = link.replace('\\/', '/')
                    
                    # Filtreleme: İçinde 'atv' geçmeli ve reklam linki olmamalı
                    if "atv" in clean_link.lower() and "m3u8" in clean_link:
                        # Eğer link 'daioncdn' içeriyorsa ama sonunda token yoksa geçebiliriz
                        # Çünkü o zaten senin yedek linkinle aynı kapıya çıkar
                        if "daioncdn" in clean_link and "?" not in clean_link:
                            continue
                            
                        print(f"🎯 Hedef bulundu: {clean_link[:50]}...")
                        return clean_link
        except Exception as e:
            print(f"⚠️ {url} adresinde hata: {e}")
            continue
            
    return None

# Yazma işlemi
new_link = get_atv_link()
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if new_link:
        f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{new_link}")
        print("✅ Liste güncel link ile yenilendi.")
    else:
        # Link bulunamazsa eski linki değil, en azından sabit kaynağı bırak
        f.write("#EXTINF:-1,ATV (Yedek - Kaynak Bulunamadi)\nhttps://atv-live.daioncdn.net/atv/atv.m3u8")
        print("❌ Hiçbir kaynaktan link çekilemedi, yedek yazıldı.")
