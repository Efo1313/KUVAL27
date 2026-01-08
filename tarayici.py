import requests

def canli_kanal_hazirla():
    # Genişletilmiş Sunucu Listesi (Farklı medya gruplarının CDN yapıları)
    sunucular = [
        {"url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/", "adi": "TURKUVAZ_GRUP"},
        {"url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/", "adi": "NOW_STAR_GRUP"},
        {"url": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/", "adi": "KANAL_D_SHOW_GRUP"},
        {"url": "https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx/", "adi": "KANAL_7_GRUP"},
        {"url": "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/", "adi": "HABERTURK_GRUP"},
        {"url": "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/", "adi": "TV8_GRUP"},
        {"url": "https://trthls.akamaized.net/hls/live/", "adi": "TRT_GRUP"} # TRT için özel CDN
    ]
    
    # Ulusal, Haber ve Spor kanalları kalıpları
    kanal_kaliplari = [
        # --- ULUSAL KANALLAR ---
        "atv/atv_1080p", "kanald/kanald_1080p", "showtv/showtv_1080p", 
        "nowtv/nowtv", "tv8/tv8_1080p", "star/startv", "kanal7/kanal7_1080p",
        "trt1/trt1_1080p", "a2tv/a2tv_720p", "teve2/teve2_720p", "beyaztv/beyaztv_720p",
        "ulusal_tv/ulusal_tv_720p", "tgrt_haber/tgrt_haber_720p",
        
        # --- HABER KANALLARI ---
        "haberturktv/haberturktv_1080p", "ahaber/ahaber_1080p", "ntv/ntv_1080p", 
        "cnnturk/cnnturk_1080p", "trthaber/trthaber_1080p", "haber_global/haber_global_1080p",
        "tvnet/tvnet_720p", "24_tv/24_tv_720p", "szctv/szctv_1080p", "halktv/halktv_1080p",
        
        # --- SPOR VE ÇOCUK ---
        "aspor/aspor_1080p", "beinsports_haber/beinsports_720p", "trtsporyildiz/trtsporyildiz_1080p",
        "minikago_cocuk/minikago_cocuk_720p", "minikago/minikago_720p", "trtcocuk/trtcocuk_1080p"
    ]
    
    yeni_liste = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("📡 Türkiye Ulusal ve Haber Ağı Taranıyor...\n")

    with requests.Session() as s:
        s.headers.update(headers)
        for sunucu in sunucular:
            for kalip in kanal_kaliplari:
                # TRT ve diğerleri için URL yapısını uyumlu hale getirme
                base_url = sunucu['url']
                test_url = f"{base_url}{kalip}.m3u8"
                
                try:
                    r = s.head(test_url, timeout=2, allow_redirects=True)
                    if r.status_code == 200:
                        # İsim temizleme (Örn: haberturktv_1080p -> HABERTURKTV)
                        kanal_adi = kalip.split("/")[-1].replace("_1080p", "").replace("_720p", "").replace("_", " ").upper()
                        
                        entry = f"#EXTINF:-1,{kanal_adi}\n{test_url}\n"
                        if entry not in yeni_liste:
                            yeni_liste.append(entry)
                            print(f"✅ AKTİF: {kanal_adi}")
                except:
                    continue

    with open("tam_kanal_listesi.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    
    print(f"\n🚀 İşlem Tamam! {len(yeni_liste)-1} kanal başarıyla listelendi.")
    print("📂 Dosya adı: tam_kanal_listesi.m3u")

if __name__ == "__main__":
    canli_kanal_hazirla()
