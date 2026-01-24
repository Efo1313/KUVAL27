import requests

# SUNUCULAR
SUNUCULAR = [
    "http://65.108.239.207/",
    "http://116.202.238.88/"
]

# KANALLAR
KANALLAR = [
    "TRT1_TR", "SHOWTV_TR", "ATV_TR", "TV8_TR", "FOXTV_TR", "NOW_TR", 
    "STAR_TR", "KANALD_TR", "TV8.5_TR", "TRTHABER_TR", "HABERTURK_TR", 
    "CNNTURK_TR", "A_HABER_TR", "TGRTHABER_TR", "Kanal7_TR", "ULKE_TR",
    "natgeo", "natgeowild", "national", "bbc", "bbcearth",
    "box1", "box2", "box3", "bsstars", "bsaction1", "bspremier1", 
    "viasathistory", "tarihtv", "discovery", "discovery2"
]

def avla():
    ganimetler = []
    # User-Agent: Bazı sunucular botları engellediği için tarayıcı taklidi yapıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    print("🦅 Avcı taramaya başladı...")

    for sunucu in SUNUCULAR:
        base_url = sunucu if sunucu.endswith('/') else sunucu + '/'
        
        for kanal in KANALLAR:
            url = f"{base_url}{kanal}/index.m3u8"
            try:
                # Sadece başlığı kontrol et, timeout'u 5 saniye yaparak daha güvenli hale getir
                r = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
                
                if r.status_code == 200:
                    temiz_isim = kanal.replace("_TR", "").upper()
                    ganimetler.append(f"#EXTINF:-1, {temiz_isim}\n{url}")
                    print(f"🎯 Bulundu: {temiz_isim}")
            except Exception:
                continue

    # Listeyi oluştur
    if ganimetler:
        with open("avci_listesi.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(ganimetler))
        print(f"✅ İşlem tamamlandı. {len(ganimetler)} kanal kaydedildi.")
    else:
        print("⚠️ Hiç canlı yayın bulunamadı.")

if __name__ == "__main__":
    avla()
