import requests
import re

# Canlı TV sayfasının URL'si
target_url = "https://m.canlitv.direct/atvcanli-yayin-izle"

def get_live_link():
    response = requests.get(target_url)
    # Sayfa kaynağından m3u8 linkini regex ile çekiyoruz
    match = re.search(r'https://.*?\.m3u8\?tkn=[^"\']+', response.text)
    if match:
        return match.group(0)
    return None

new_link = get_live_link()

if new_link:
    with open("atv_listesi.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canlı\n{new_link}")
    print("Link başarıyla güncellendi!")
