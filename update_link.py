import cloudscraper
import re

def get_tel_link(path):
    scraper = cloudscraper.create_scraper()
    # Sitenin ana yayın sayfası
    url = f"https://www.canlitv.tel/{path}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.canlitv.tel/"
    }

    try:
        print(f"Kaynak taranıyor: {url}")
        response = scraper.get(url, headers=headers, timeout=15)
        
        # HTML içindeki hash'li m3u8 linkini yakala
        # Hem 'file' hem 'source' hem de tırnak içindeki linkleri tarar
        match = re.search(r'["\'](https?://[^"\']+\.m3u8\?hash=[^"\']+)["\']', response.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except Exception as e:
        print(f"Hata: {e}")
    return None

# Kanalları tara
atv_link = get_tel_link("atv-canli")
a2_link = get_tel_link("a2-tv-canli-izle") # Sitedeki slug'a göre düzenledim

# M3U Dosyasını oluştur
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if atv_link:
        f.write(f"#EXTINF:-1,ATV Canli\n{atv_link}\n")
    if a2_link:
        f.write(f"#EXTINF:-1,A2 TV Canli\n{a2_link}\n")

print(f"İşlem tamam! Yeni Link: {atv_link}")
