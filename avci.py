import requests

# SUNUCULAR
SUNUCULAR = [
    "http://65.108.239.207/",
    "http://116.202.238.88/"
]

# GENİŞLETİLMİŞ TÜRK KANALLARI VE DİĞERLERİ
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
    print("🦅 Avci taramaya basladi...")

    for sunucu in SUNUCULAR:
        for kanal in KANALLAR:
            url = f"{sunucu}{kanal}/index.m3u8"
            try:
                r = requests.head(url, timeout=3, allow_redirects=True)
                if r.status_code == 200:
                    # İsim temizleme: _TR'yi kaldır ve büyük harf yap
                    temiz_isim = kanal.replace("_TR", "").upper()
                    ganimetler.append(f"#EXTINF:-1, {temiz_isim}\n{url}")
                    print(f"🎯 Bulundu: {temiz_isim}")
            except:
                continue

    # Listeyi oluştur
    with open("avci_listesi.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(ganimetler))
    
    print(f"✅ Islem tamamlandi. {len(ganimetler)} kanal kaydedildi.")

if __name__ == "__main__":
    avla()
