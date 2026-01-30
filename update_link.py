import cloudscraper
import re

def scrape_deep(kanal_slug):
    # Sitenin korumasını geçmek için tarayıcıyı taklit et
    scraper = cloudscraper.create_scraper()
    
    # Doğrudan yayın motorunun olduğu sayfayı hedef al
    base_urls = [
        f"https://m.canlitv.direct/yayin.php?kanal={kanal_slug}",
        f"https://m.canlitv.direct/{kanal_slug}"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "https://m.canlitv.direct/"
    }

    for url in base_urls:
        try:
            print(f"Denetleniyor: {url}")
            res = scraper.get(url, headers=headers, timeout=15)
            # Linkler bazen 'source: "..." ' veya 'file: "..." ' içinde gizlidir
            # Kaçış karakterli (slashed) m3u8'leri yakala
            match = re.search(r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']', res.text)
            if match:
                link = match.group(1).replace('\\/', '/')
                if "atv" in link.lower() or "a2tv" in link.lower():
                    return link
        except:
            continue
    return None

# Kanal isimlerini sitenin kullandığı slug yapısına göre çek
atv_link = scrape_deep("atvcanli-yayin-izle")
a2_link = scrape_deep("a2-tv-canli-izle")

# M3U Dosyasını oluştur
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    # ATV
    if atv_link:
        f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{atv_link}\n")
    else:
        f.write("#EXTINF:-1,ATV (Yedek)\nhttps://atv-live.daioncdn.net/atv/atv.m3u8\n")
        
    # A2 TV
    if a2_link:
        f.write(f"#EXTINF:-1,A2 TV Canli (Guncel)\n{a2_link}\n")
    else:
        f.write("#EXTINF:-1,A2 TV (Yedek)\nhttps://trkvz-live.daioncdn.net/a2tv/a2tv.m3u8\n")

print("İşlem tamamlandı, dosyayı kontrol et.")
