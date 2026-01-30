import requests
import re

def get_channel_link(channel_name):
    # Dünya çapındaki en büyük, doğrulanmış IPTV havuzu
    api_url = "https://iptv-org.github.io/iptv/countries/tr.m3u"
    
    try:
        print(f"{channel_name} aranıyor...")
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for i, line in enumerate(lines):
                # Kanal ismini içeren satırı bul
                if "#EXTINF" in line and channel_name.upper() in line.upper():
                    # Bir sonraki satır linktir
                    link = lines[i+1].strip()
                    if link.startswith("http"):
                        return link
    except Exception as e:
        print(f"Hata: {e}")
    return None

# Kanalları çek
atv = get_channel_link("ATV")
a2 = get_channel_link("A2")

# Dosyayı yaz
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{atv if atv else 'https://atv-live.daioncdn.net/atv/atv.m3u8'}\n")
    f.write(f"#EXTINF:-1,A2 TV Canli\n{a2 if a2 else 'https://trkvz-live.daioncdn.net/a2tv/a2tv.m3u8'}\n")

print(f"Bitti! ATV: {atv} | A2: {a2}")
