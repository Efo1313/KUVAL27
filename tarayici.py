import requests

def tek_liste_hazirla():
    # TRT, TV100, SZC ve Halk TV gibi tüm sunucular eklendi
    veri_yapisi = [
        # --- TURKUVAZ GRUBU ---
        {"sunucu": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo", "kanallar": ["atv/atv_1080p", "ahaber/ahaber_1080p", "aspor/aspor_1080p", "a2tv/a2tv_720p", "minikago/minikago_720p"]},
        # --- STAR & NOW ---
        {"sunucu": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw", "kanallar": ["nowtv/nowtv", "startv/startv"]},
        # --- KANAL D & SHOW TV ---
        {"sunucu": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba", "kanallar": ["kanald/kanald_1080p", "showtv/showtv_1080p"]},
        # --- KANAL 7 GRUBU ---
        {"sunucu": "https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx", "kanallar": ["kanal7/kanal7_1080p", "ulketv/ulketv_1080p"]},
        # --- HABERTÜRK & BLOOMBERG ---
        {"sunucu": "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp", "kanallar": ["haberturktv/haberturktv_1080p", "bloomberght/bloomberght_720p"]},
        # --- TV8 GRUBU ---
        {"sunucu": "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof", "kanallar": ["tv8/tv8_1080p", "tv8_5/tv8_5_1080p"]},
        # --- BAĞIMSIZ HABER KANALLARI ---
        {"sunucu": "https://tv100.ercdn.net/tv100", "kanallar": ["tv100"]},
        {"sunucu": "https://szc.ercdn.net/szc", "kanallar": ["szc_1080p"]},
        {"sunucu": "https://haberglobal.ercdn.net/haberglobal", "kanallar": ["haberglobal_1080p"]},
        {"sunucu": "https://halktv.ercdn.net/halktv", "kanallar": ["halktv_1080p"]},
        # --- TRT PAKETİ (Akamai Sunucusu) ---
        {"sunucu": "https://trthls.akamaized.net/hls/live", "kanallar": ["718012/trt1_1080p", "718013/trthaber_1080p", "718015/trtsporyildiz_1080p", "718021/trtcocuk_1080p"]}
    ]

    yeni_liste = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print("📡 Tüm Türkiye ağ taranıyor (Haber + Ulusal + TRT)...")

    with requests.Session() as s:
        s.headers.update(headers)
        for grup in veri_yapisi:
            for kalip in grup["kanallar"]:
                test_url = f"{grup['sunucu']}/{kalip}.m3u8"
                try:
                    r = s.get(test_url, timeout=4, stream=True)
                    if r.status_code == 200:
                        # İsim temizleme (Sayıları ve uzantıları atar)
                        kanal_adi = kalip.split("/")[-1].replace("_1080p", "").replace("_720p", "").replace("_", " ").upper()
                        # TRT için özel isim temizleme
                        if "TRT" in kanal_adi: kanal_adi = kanal_adi.split("_")[0].upper()
                        
                        yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{test_url}\n")
                        print(f"✅ AKTİF: {kanal_adi}")
                    r.close()
                except:
                    continue

    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    
    print(f"\n🚀 Liste Tamamlandı! Toplam {len(yeni_liste)-1} kanal aktif.")

if __name__ == "__main__":
    tek_liste_hazirla()
