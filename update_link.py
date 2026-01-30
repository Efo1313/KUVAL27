import cloudscraper
import re

def link_avcisi(kanal_slug):
    scraper = cloudscraper.create_scraper()
    # Farklı kaynakları aynı anda tara
    kaynaklar = [
        f"https://m.canlitv.direct/{kanal_slug}",
        f"https://www.canlitv.vin/{kanal_slug.replace('canli-yayin-izle', 'izle')}",
        f"https://canlitvizle.com/{kanal_slug}"
    ]
    
    headers = {"Referer": "https://google.com"}

    for url in kaynaklar:
        try:
            print(f"Aranıyor: {url}")
            res = scraper.get(url, headers=headers, timeout=10)
            # m3u8 linkini ve beraberindeki tokeni yakala
            match = re.search(r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']', res.text)
            if match:
                return match.group(1).replace('\\/', '/')
        except:
            continue
    return None

# Kanalları tara
atv = link_avcisi("atvcanli-yayin-izle")
a2 = link_avcisi("a2-tv-canli-izle")

# Sonucu ekrana bas ve dosyaya yaz
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{atv if atv else 'Bulunamadi'}\n")
    f.write(f"#EXTINF:-1,A2 TV Canli\n{a2 if a2 else 'Bulunamadi'}\n")

print("\n--- İŞLEM TAMAM ---")
print(f"ATV: {atv}")
print(f"A2: {a2}")
