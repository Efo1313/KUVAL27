import requests
import re
import os

def get_atv_link():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://www.atv.com.tr/"
    }
    
    # Farklı mimarilere sahip kaynaklar
    sources = [
        "https://canlitv.com/atv-canli-yayini-izle",
        "https://www.canlitv.vin/atv-izle",
        "https://canlitvizle.com/atv-canli-yayin-izle-1",
        "https://m.canlitv.direct/atv-canli-izle"
    ]

    print("--- Derin Tarama Başlatıldı ---")

    for url in sources:
        try:
            print(f"Kaynak: {url}")
            # Bazı siteler requests'i engellerse diye sessizce geçiyoruz
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200: continue

            # Regex: Tırnaklı, tırnaksız veya kaçış karakterli tüm m3u8'leri bul
            links = re.findall(r'(https?[:\\]+(?:[^\s"\']+\.m3u8(?:[^\s"\']*)))', res.text)
            
            for link in links:
                clean_link = link.replace('\\/', '/').replace('\\', '').strip('"\',')
                
                # Linkin içinde 'atv' geçmeli ve 'daioncdn' tek başına (tokensiz) olmamalı
                if "atv" in clean_link.lower() and ".m3u8" in clean_link:
                    # Kendi statik linkimizi (çalışmayan) elemek için:
                    if "atv-live.daioncdn.net/atv/atv.m3u8" in clean_link and "?" not in clean_link:
                        continue
                    
                    print(f"🎯 Potansiyel Link: {clean_link}")
                    return clean_link
        except:
            continue
    return None

# Yazma işlemi
new_link = get_atv_link()
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if new_link:
        f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{new_link}")
        print("✅ GÜNCELLENDİ!")
    else:
        # Hiçbiri olmazsa linki boş bırakma, en azından manuel girilecek bir yer kalsın
        f.write("#EXTINF:-1,ATV (Yedek - Kaynak Bulunamadi)\nhttps://atv-live.daioncdn.net/atv/atv.m3u8")
        print("❌ BAŞARISIZ: Tüm kaynaklar kapalı.")
