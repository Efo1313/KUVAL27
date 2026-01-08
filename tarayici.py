import requests

def canli_kanal_hazirla():
    # Senin verdiğin ve yeni eklediğimiz CDN sunucuları
    sunucular = [
        {"url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/", "adi": "TURKUVAZ_ATV"},
        {"url": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/", "adi": "KANALD_SHOW"},
        {"url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/", "adi": "NOW_STAR"},
        {"url": "https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx/", "adi": "KANAL_7"},
        {"url": "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/", "adi": "HABERTURK"},
        {"url": "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/", "adi": "TV8_GRUP"}
    ]
    
    # Tüm Ulusal ve Haber kanallarının kalıpları
    kanal_kaliplari = [
        # --- ANA ULUSAL KANALLAR ---
        "atv/atv_1080p", "kanald/kanald_1080p", "showtv/showtv_1080p", 
        "nowtv/nowtv", "tv8/tv8_1080p", "star/startv", "kanal7/kanal7_1080p",
        "a2tv/a2tv_720p", "teve2/teve2_720p", "beyaztv/beyaztv_720p",
        
        # --- HABER KANALLARI ---
        "haberturktv/haberturktv_1080p", "ahaber/ahaber_1080p", "ntv/ntv_1080p", 
        "cnnturk/cnnturk_1080p", "haber_global/haber_global_1080p", "tgrt_haber/tgrt_haber_720p",
        "szctv/szctv_1080p", "halktv/halktv_1080p", "tvnet/tvnet_720p",
        
        # --- SPOR VE DİĞER ---
        "aspor/aspor_1080p", "minikago/minikago_720p", "minikago_cocuk/minikago_cocuk_720p"
    ]
    
    yeni_liste = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("📡 Ulusal ve Haber kanalları taranıyor...\n")

    with requests.Session() as s:
        s.headers.update(headers)
        for sunucu in sunucular:
            for kalip in kanal_kaliplari:
                test_url = f"{sunucu['url']}{kalip}.m3u8"
                try:
                    # Hızlı kontrol için head isteği ve 2 saniye timeout
                    r = s.head(test_url, timeout=2, allow_redirects=True)
                    if r.status_code == 200:
                        # İsimdeki karmaşayı temizle (Örn: kanald_1080p -> KANAL D)
                        kanal_adi = kalip.split("/")[-1].split("_")[0].upper()
                        
                        entry = f"#EXTINF:-1,{kanal_adi}\n{test_url}\n"
                        if entry not in yeni_liste:
                            yeni_liste.append(entry)
                            print(f"✅ AKTİF: {kanal_adi}")
                except:
                    continue

    with open("guncel_kanallarim.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    
    print(f"\n🚀 Liste hazır! 'guncel_kanallarim.m3u' dosyasına {len(yeni_liste)-1} kanal kaydedildi.")

if __name__ == "__main__":
    canli_kanal_hazirla()
