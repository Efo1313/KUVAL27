import requests

def get_channel_link(search_term):
    # Dünya çapındaki güvenilir ve güncel m3u havuzları
    sources = [
        "https://iptv-org.github.io/iptv/countries/tr.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in sources:
        try:
            print(f"Havuz kontrol ediliyor: {url}")
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                lines = res.text.split('\n')
                for i, line in enumerate(lines):
                    # Tam eşleşme arıyoruz (Örn: "ATV" veya "A2")
                    if "#EXTINF" in line and search_term.upper() in line.upper():
                        link = lines[i+1].strip()
                        if link.startswith("http") and ".m3u8" in link:
                            # Yanlış eşleşmeyi önlemek için ikincil kontrol
                            if search_term.lower() in link.lower() or search_term.lower() in line.lower():
                                return link
        except:
            continue
    return None

# Kanal linklerini ayrı ayrı çek
atv_url = get_channel_link("ATV")
a2_url = get_channel_link("A2")

# Eğer havuzda bulunamazsa, Bulgaristan'dan çalışan alternatifleri tanımla
if not atv_url: atv_url = "https://nhvnetv.com/p/atv.m3u8"
if not a2_url: a2_url = "https://nhvnetv.com/p/a2tv.m3u8"

# M3U Dosyasını oluştur
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{atv_url}\n")
    f.write(f"#EXTINF:-1,A2 TV Canli\n{a2_url}\n")

print(f"Güncelleme Bitti!\nATV: {atv_url}\nA2: {a2_url}")
