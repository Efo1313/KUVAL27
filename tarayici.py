import requests

def canli_kanal_hazirla():
    # TV8'in yeni sunucusu dahil tüm kaynaklar
    sunucular = [
        {"url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/", "adi": "TURKUVAZ"},
        {"url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/", "adi": "NOW_STAR"},
        {"url": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/", "adi": "KANAL_D_SHOW"},
        {"url": "https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx/", "adi": "KANAL_7"},
        {"url": "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/", "adi": "HABERTURK"},
        {"url": "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/", "adi": "TV8_GRUP"} # Yeni TV8 Sunucusu
    ]
    
    # Denenecek kanal isimleri
    kanal_kaliplari = [
        "atv/atv_1080p", "aspor/aspor_1080p", "a2tv/a2tv_720p",
        "nowtv/nowtv", "kanald/kanald_1080p", "kanal7/kanal7_1080p",
        "haberturktv/haberturktv_1080p", "tv8/tv8_1080p", # TV8 eklendi
        "minikago_cocuk/minikago_cocuk_720p", "minikago/minikago_720p",
        "showtv/showtv_1080p", "startv/startv"
    ]
    
    yeni_liste = ["#EXTM3U\n"]
    print("TV8 ve HaberTürk dahil tüm ağ taranıyor...")

    for sunucu in sunucular:
        for kalip in kanal_kaliplari:
            test_url = f"{sunucu['url']}{kalip}.m3u8"
            try:
                # 3 saniyelik kontrol
                r = requests.head(test_url, timeout=3)
                if r.status_code == 200:
                    # İsim düzenleme
                    kanal_adi = kalip.split("/")[-1].replace("_1080p", "").replace("_720p", "").replace("_", " ").upper()
                    if f"{test_url}\n" not in yeni_liste:
                        yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{test_url}\n")
                        print(f"✅ AKTİF: {kanal_adi}")
            except:
                continue

    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    print(f"\n✅ TV8 başarıyla sisteme entegre edildi!")

if __name__ == "__main__":
    canli_kanal_hazirla()
