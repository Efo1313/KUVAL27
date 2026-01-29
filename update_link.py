import requests
import re

def get_alternative_link():
    # Player 2 veya Player 3'ün kullandığı gizli embed yapısı
    # Site genellikle kanalları bu şekilde dışarı açar
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        "Referer": "https://m.canlitv.direct/"
    }
    
    # Denenecek alternatif player yolları
    alternatives = [
        "https://m.canlitv.direct/yayin.php?kanal=atvcanli-yayin-izle",
        "https://m.canlitv.direct/kanallar.php?kanal=atvcanli-yayin-izle",
        "https://m.canlitv.direct/atvcanli-yayin-izle/2"
    ]

    for url in alternatives:
        try:
            print(f"Deneniyor: {url}")
            res = requests.get(url, headers=headers, timeout=10)
            # m3u8 linkini ara
            match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', res.text)
            if match:
                return match.group(1).replace('\\/', '/')
        except:
            continue
    return None

new_link = get_alternative_link()

# M3U Dosyasını Güncelle
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    if new_link:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canli\n{new_link}")
        print(f"Bulunan Alternatif Link: {new_link}")
    else:
        # EĞER HİÇBİRİ ÇALIŞMAZSA: Bilinen en kararlı ATV stream adresini manuel ekle
        # Bu link genelde çok uzun süre değişmez
        fallback = "https://atv-live.daioncdn.net/atv/atv.m3u8"
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV (Yedek)\n{fallback}")
        print("Bot engellendi, yedek link eklendi.")
