import cloudscraper
import re

def get_vin_link(slug):
    scraper = cloudscraper.create_scraper()
    # Sitenin yayın sayfası
    url = f"https://www.canlitv.vin/{slug}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.canlitv.vin/"
    }

    try:
        print(f"Kaynak taranıyor: {url}")
        response = scraper.get(url, headers=headers, timeout=15)
        
        # HTML içinde m3u8?tkn= ile başlayan linki ara
        match = re.search(r'["\'](https?://[^"\']+\.m3u8\?tkn=[^"\']+)["\']', response.text)
        if match:
            link = match.group(1).replace('\\/', '/')
            return link
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

# Kanalları al
atv_link = get_vin_link("atv-izle")
a2_link = get_vin_link("a2-tv-izle")

# M3U Dosyasını oluştur
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if atv_link:
        f.write(f"#EXTINF:-1,ATV Canli\n{atv_link}\n")
    if a2_link:
        f.write(f"#EXTINF:-1,A2 TV Canli\n{a2_link}\n")

print(f"İşlem tamam! Yeni ATV linki: {atv_link}")
