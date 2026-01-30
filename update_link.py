import cloudscraper
import re
import os

def get_atv_link():
    # Chrome tarayıcıyı birebir taklit eden session
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    # Daha geniş ve güncel kaynak havuzu
    sources = [
        "https://canlitv.center/atv-canli-yayin",
        "https://www.canlitv.vin/atv-izle",
        "https://m.canlitv.me/atv-canli-izle-1",
        "https://www.canlitv.today/atv-canli-yayin-izle-1"
    ]
    
    # Regex: Hem standart hem de şifrelenmiş olabilecek m3u8 linklerini yakalar
    # (Token içeren dinamik linkleri önceliklendirir)
    m3u8_pattern = r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']'

    print("--- ATV Canlı Yayın Avı Başlatıldı ---")

    for url in sources:
        try:
            # Her site için özel referer göndererek güvenliği aşmayı dene
            headers = {"Referer": url}
            print(f"Sorgulanıyor: {url}")
            response = scraper.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                html_content = response.text
                matches = re.findall(m3u8_pattern, html_content)
                
                for link in matches:
                    clean_link = link.replace('\\/', '/')
                    
                    # Filtreleme kriterleri:
                    # 1. İçinde 'atv' geçmeli
                    # 2. Sadece 'daioncdn' olup tokensiz olan (yani senin çalışmayan linkin) olmamalı
                    if "atv" in clean_link.lower() and "m3u8" in clean_link:
                        if "daioncdn" in clean_link and "?" not in clean_link:
                            continue # Bu link muhtemelen çalışmayan ham linktir, atla.
                        
                        print(f"🎯 Aktif Link Yakalandı: {clean_link}")
                        return clean_link
        except Exception as e:
            continue
            
    return None

# Yazma işlemi
new_link = get_atv_link()
file_path = "atv_listesi.m3u"

with open(file_path, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if new_link:
        f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{new_link}")
        print("✅ Başarıyla güncellendi.")
    else:
        # Link bulunamazsa, en azından bir ihtimal çalışabilecek resmi web parametresini ekle
        f.write("#EXTINF:-1,ATV (Yedek - Kaynak Bulunamadi)\nhttps://atv-live.daioncdn.net/atv/atv.m3u8")
        print("❌ Kaynaklar korumalı, manuel müdahale gerekebilir.")
