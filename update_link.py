import requests
import re

def get_atv_link():
    # Bulgaristan veya GitHub üzerinden erişilebilen, yurt dışı kısıtlaması daha esnek kaynaklar
    sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
        "https://www.canlitv.me/atv-canli-izle-1",
        "https://trkvz-live.ercdn.net/atv/atv_720p.m3u8" # Yedek CDN
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.atv.com.tr/"
    }

    print("--- Bulgaristan / Yurt Dışı Taraması Başlatıldı ---")

    for url in sources:
        try:
            # Eğer kaynak bir m3u8 dosyasıysa doğrudan döndür
            if url.endswith(".m3u8"):
                return url
                
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                # Sayfa içindeki gizli m3u8'leri ayıkla
                match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', res.text)
                if match:
                    link = match.group(1).replace('\\/', '/')
                    if "atv" in link.lower():
                        return link
        except:
            continue
    
    # Hiçbiri olmazsa yurt dışında en kararlı çalışan Avrupa CDN linki
    return "https://trkvz-live.ercdn.net/atv/atv.m3u8"

# Yazma işlemi
new_link = get_atv_link()
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli (Bulgaristan Uyumlu)\n{new_link}")

print(f"Bitti! Yazılan Link: {new_link}")
