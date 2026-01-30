import requests

def get_verified_link(channel_key):
    # Bulgaristan'dan erişilebilen ve sık güncellenen global havuzlar
    # ATV ve A2 için farklı kaynakları tarar
    sources = [
        "https://iptv-org.github.io/iptv/countries/tr.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in sources:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                lines = res.text.split('\n')
                for i, line in enumerate(lines):
                    if "#EXTINF" in line and channel_key.upper() in line.upper():
                        link = lines[i+1].strip()
                        if link.startswith("http") and ".m3u8" in link:
                            return link
        except:
            continue
    return None

# Linkleri Tek Tek Al (Karışmaması için ayrı değişkenler)
atv_link = get_verified_link("ATV")
a2_link = get_verified_link("A2")

# Eğer havuzda bulunamazsa, Bulgaristan'dan en stabil açılan yedekleri manuel tanımla
if not atv_link: atv_link = "https://nhvnetv.com/p/atv.m3u8"
if not a2_link: a2_link = "https://nhvnetv.com/p/a2tv.m3u8"

# M3U Dosyasını Yaz
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{atv_link}\n")
    f.write(f"#EXTINF:-1,A2 TV Canli\n{a2_link}\n")

print(f"Güncelleme Tamamlandı!\nATV: {atv_link}\nA2: {a2_link}")
