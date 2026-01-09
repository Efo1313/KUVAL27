import requests
import urllib3

# SSL uyarılarını kapatmak için (Sertifika hatalarını engeller)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tek_liste_hazirla():
    veri_yapisi = [
        # --- TURKUVAZ GRUBU ---
        {"sunucu": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo", "kanallar": ["atv/atv_1080p", "ahaber/ahaber_1080p", "aspor/aspor_1080p", "a2tv/a2tv_720p", "minikago/minikago_720p"]},
        # --- KANAL D & SHOW TV (Güncel Ercdn) ---
        {"sunucu": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba", "kanallar": ["kanald/kanald_1080p", "showtv/showtv_1080p"]},
        # --- HABERTÜRK ---
        {"sunucu": "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp", "kanallar": ["haberturktv/haberturktv_1080p", "bloomberght/bloomberght_720p"]},
        # --- TV8 GRUBU ---
        {"sunucu": "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof", "kanallar": ["tv8/tv8_1080p", "tv8_5/tv8_5_1080p"]},
        # --- BAĞIMSIZLAR ---
        {"sunucu": "https://tv100.ercdn.net/tv100", "kanallar": ["tv100"]},
        {"sunucu": "https://szc.ercdn.net/szc", "kanallar": ["szc_1080p"]},
        {"sunucu": "https://halktv.ercdn.net/halktv", "kanallar": ["halktv_1080p"]},
        # --- TRT PAKETİ (Sabit Akamai) ---
        {"sunucu": "https://trthls.akamaized.net/hls/live", "kanallar": ["718012/trt1_1080p", "718013/trthaber_1080p", "718015/trtsporyildiz_1080p", "718021/trtcocuk_1080p"]}
    ]

    yeni_liste = ["#EXTM3U\n"]
    # Daha profesyonel bir header yapısı
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    print("📡 Ulusal Kanallar Kontrol Ediliyor...")

    with requests.Session() as s:
        s.headers.update(headers)
        for grup in veri_yapisi:
            for kalip in grup["kanallar"]:
                test_url = f"{grup['sunucu']}/{kalip}.m3u8"
                try:
                    # verify=False ekleyerek SSL hatalarını geçiyoruz
                    r = s.get(test_url, timeout=5, stream=True, verify=False)
                    
                    if r.status_code == 200:
                        # İsim temizleme algoritması
                        ham_isim = kalip.split("/")[-1]
                        temiz_isim = ham_isim.replace("_1080p", "").replace("_720p", "").replace("_", " ").upper()
                        
                        # TRT Sayısal isimleri düzeltme
                        if "718012" in temiz_isim: temiz_isim = "TRT 1"
                        if "718013" in temiz_isim: temiz_isim = "TRT HABER"
                        if "718015" in temiz_isim: temiz_isim = "TRT SPOR YILDIZ"
                        if "718021" in temiz_isim: temiz_isim = "TRT COCUK"
                        
                        yeni_liste.append(f"#EXTINF:-1,{temiz_isim}\n{test_url}\n")
                        print(f"✅ AKTİF: {temiz_isim}")
                    else:
                        print(f"❌ ÇALIŞMIYOR: {temiz_isim} (Kod: {r.status_code})")
                    r.close()
                except Exception as e:
                    print(f"⚠️ HATA: {test_url} bağlantı kurulamadı.")
                    continue

    # Dosyaya yazma
    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    
    print(f"\n🚀 Liste Tamamlandı! {len(yeni_liste)-1} kanal canli_tv_listem.m3u dosyasına yazıldı.")

if __name__ == "__main__":
    tek_liste_hazirla()
