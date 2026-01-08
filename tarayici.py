import requests

def canli_kanal_hazirla():
    # Turknet'in iki ana sunucu merkezi
    sunucular = [
        {"url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/", "adi": "TURKUVAZ"},
        {"url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/", "adi": "NOW_GRUP"}
    ]
    
    # Denenecek tüm muhtemel kanal kalıpları
    kanal_kaliplari = [
        "atv/atv_1080p", "ahaber/ahaber_1080p", "aspor/aspor_1080p",
        "nowtv/nowtv", "minikago_cocuk/minikago_cocuk_720p", 
        "minikacocuk/minikacocuk_720p", "apara/apara_1080p",
        "minikago/minikago_720p", "a2tv/a2tv_720p"
    ]
    
    yeni_liste = ["#EXTM3U\n"]
    print("Geniş kapsamlı kanal taraması başlatıldı...")

    for sunucu in sunucular:
        for kalip in kanal_kaliplari:
            test_url = f"{sunucu['url']}{kalip}.m3u8"
            try:
                # Sadece linkin varlığını kontrol et
                r = requests.head(test_url, timeout=5)
                if r.status_code == 200:
                    # İsim temizleme: minikago_cocuk -> MINIKA GO COCUK
                    kanal_adi = kalip.split("/")[-1].replace("_", " ").upper()
                    yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{test_url}\n")
                    print(f"Başarıyla eklendi: {kanal_adi}")
            except:
                continue

    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    print("\nİşlem tamam! canli_tv_listem.m3u güncellendi.")

if __name__ == "__main__":
    canli_kanal_hazirla()
