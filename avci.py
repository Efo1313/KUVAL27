import requests

# AV SAHASI (Senin verdiğin iki ana merkez)
SUNUCULAR = [
    "http://65.108.239.207/",
    "http://116.202.238.88/"
]

# AV POTANSİYELİ (Bu isimleri ve varyasyonlarını tarayacak)
AD_TASLAKLARI = [
    "bsstars", "bsaction", "bspremier", "box", "tarihtv", "viasathistory", "discovery",
    "TRT1_TR", "SHOWTV_TR", "ATV_TR", "TV8_TR", "FOXTV_TR", "TRTHABER_TR", "CNNTURK_TR",
    "KANALD_TR", "STAR_TR", "TV8.5_TR", "BELGESEL", "SPOR", "SINEMA"
]

def tum_kanallari_cikar():
    bulunan_ganimetler = []
    print("🦅 Avcı sunucuların içine sızıyor, tüm kanallar çıkartılıyor...")

    for sunucu in SUNUCULAR:
        for taslak in AD_TASLAKLARI:
            # Hem normal ismini hem de sonuna 1, 2, 3 ekleyerek dene
            for i in range(1, 5):
                suffix = "" if i == 1 else str(i)
                # Bazı sunucular direkt ismi kullanır, bazıları sonuna numara ekler
                test_adlari = [f"{taslak}{suffix}", f"{taslak.replace('_TR', '')}{suffix}_TR"]
                
                for kanal_adi in set(test_adlari):
                    url = f"{sunucu}{kanal_adi}/index.m3u8"
                    try:
                        # Zaman aşımını kısa tutuyoruz ki hızlı tarasın
                        r = requests.head(url, timeout=1.5)
                        if r.status_code == 200:
                            print(f"🎯 Kanal Çıkartıldı: {url}")
                            bulunan_ganimetler.append(f"#EXTINF:-1, 🦅 AVCI | {kanal_adi}\n{url}")
                            break # Bu taslak için bir tane bulduysa diğer rakama geçebilir
                    except:
                        continue

    # Dosyaya Yazma
    with open("avci_listesi.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(bulunan_ganimetler))
    
    print(f"\n✅ İşlem Tamam! Toplam {len(bulunan_ganimetler)} kanal gün yüzüne çıkarıldı.")

if __name__ == "__main__":
    tum_kanallari_cikar()
