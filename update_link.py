import cloudscraper
import re

def get_live_link(target_path):
    scraper = cloudscraper.create_scraper()
    # Sitenin mobil versiyonu genellikle daha kolay link verir
    url = f"https://m.canlitv.direct/{target_path}"
    headers = {"Referer": "https://m.canlitv.direct/"}

    try:
        print(f"Kaynak taranıyor: {url}")
        response = scraper.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Sayfa içindeki gerçek m3u8'i (tokenlı haliyle) bul
            match = re.search(r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']', response.text)
            if match:
                return match.group(1).replace('\\/', '/')
    except:
        return None
    return None

# İki kanal için de linkleri çek
atv_link = get_live_link("atvcanli-yayin-izle")
a2_link = get_live_link("a2-tv-canli-izle")

# M3U Dosyasını Oluştur
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    if atv_link:
        f.write(f"#EXTINF:-1,ATV Canli\n{atv_link}\n")
    else:
        f.write("#EXTINF:-1,ATV (Yedek)\nhttps://atv-live.daioncdn.net/atv/atv.m3u8\n")
        
    if a2_link:
        f.write(f"#EXTINF:-1,A2 TV Canli\n{a2_link}\n")
    else:
        f.write(f"#EXTINF:-1,A2 TV (Yedek)\nhttps://trkvz-live.daioncdn.net/a2tv/a2tv.m3u8\n")

print("Dosya başarıyla güncellendi!")
