import requests
import re

def get_atv_global():
    # Yurt dışından erişilebilen global IPTV havuzları (Bulgaristan uyumlu)
    global_sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
        "https://iptv-org.github.io/iptv/countries/tr.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    print("--- Global Kaynaklar Taranıyor (Bulgaristan) ---")

    for url in global_sources:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                # ATV satırını bul ve bir altındaki m3u8 linkini al
                lines = res.text.split('\n')
                for i, line in enumerate(lines):
                    if "#EXTINF" in line and "ATV" in line.upper():
                        # Bir sonraki satır linktir
                        potential_link = lines[i+1].strip()
                        if potential_link.startswith("http"):
                            print(f"🎯 Global Link Bulundu: {potential_link}")
                            return potential_link
        except:
            continue
    
    # Eğer yukarıdakiler de olmazsa, yurt dışında en kararlı çalışan m3u8 adresi
    return "https://nhvnetv.com/p/atv.m3u8" # Alternatif global provider

# Dosyaya Yaz
new_link = get_atv_global()
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli (Global-Bulgaristan)\n{new_link}")

print(f"Bitti. Yeni Link: {new_link}")
