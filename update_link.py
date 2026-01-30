import cloudscraper
import re

def get_link(slug):
    scraper = cloudscraper.create_scraper()
    url = f"https://www.canlitv.tel/{slug}"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.canlitv.tel/"}
    try:
        res = scraper.get(url, headers=headers, timeout=15)
        # m3u8?hash= desenini yakalar
        match = re.search(r'["\'](https?://[^"\']+\.m3u8\?hash=[^"\']+)["\']', res.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except:
        return None
    return None

atv = get_link("atv-canli")
a2 = get_link("a2-tv-canli-izle")

with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{atv if atv else 'https://atv-live.daioncdn.net/atv/atv.m3u8'}\n")
    f.write(f"#EXTINF:-1,A2 TV Canli\n{a2 if a2 else 'https://trkvz-live.daioncdn.net/a2tv/a2tv.m3u8'}\n")

print(f"ATV: {atv}\nA2: {a2}")
