import requests
import re
import json

def get_alternative_link():
    print("--- ATV Canlı Yayın Linki Aranıyor ---")
    
    # Gerçekçi bir tarayıcı kimliği
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://m.canlitv.direct/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webkit/sdk;q=0.8"
    }
    
    alternatives = [
        "https://m.canlitv.direct/atv-canli-izle",
        "https://m.canlitv.direct/yayin.php?kanal=atvcanli-yayin-izle",
        "https://m.canlitv.direct/atvcanli-yayin-izle/2"
    ]

    # m3u8 yakalamak için daha esnek bir Regex
    # Hem tırnak içindeki linkleri hem de kaçış karakterli (slashed) linkleri yakalar
    m3u8_pattern = r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']'

    for url in alternatives:
        try:
            print(f"Denetleniyor: {url}")
            response = requests.get(url, headers=headers, timeout=12)
            response.raise_for_status() # 404 veya 500 hatası varsa geç
            
            content = response.text
            match = re.search(m3u8_pattern, content)
            
            if match:
                raw_link = match.group(1)
                # Kaçış karakterlerini temizle (örneğin: https:\/\/ -> https://)
                clean_link = raw_link.replace('\\/', '/')
                print(f"✅ Başarılı! Link bulundu.")
                return clean_link
                
        except Exception as e:
            print(f"⚠️ Bağlantı hatası ({url}): {e}")
            continue
            
    return None

# --- Ana Çalıştırma Kısmı ---
new_link = get_alternative_link()

file_name = "atv_listesi.m3u"
try:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if new_link:
            f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{new_link}")
            print(f"\nSonuç: {file_name} başarıyla güncellendi.")
            print(f"Link: {new_link}")
        else:
            # Yedek link (Statik olduğu için her zaman çalışmayabilir)
            fallback = "https://atv-live.daioncdn.net/atv/atv.m3u8"
            f.write(f"#EXTINF:-1,ATV (Yedek - Token Gerekebilir)\n{fallback}")
            print("\n❌ Aktif link bulunamadı, yedek adres yazıldı.")
except IOError as e:
    print(f"Dosya yazma hatası: {e}")
