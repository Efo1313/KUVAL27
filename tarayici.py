import requests

def canli_kanal_hazirla():
    # Senin paylaştığın çalışan linklerin temel yapıları
    sunucu_verileri = [
        ("http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo", ["atv/atv_1080p", "aspor/aspor_1080p", "a2tv/a2tv_720p", "minikago_cocuk/minikago_cocuk_720p", "minikago/minikago_720p"]),
        ("https://uycyyuuzyh.turknet.ercdn.net/nphindgytw", ["nowtv/nowtv"]),
        ("https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba", ["kanald/kanald_1080p"]),
        ("https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx", ["kanal7/kanal7_1080p"]),
        ("https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp", ["haberturktv/haberturktv_1080p"]),
        ("https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof", ["tv8/tv8_1080p"])
    ]
    
    yeni_liste = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    print("🚀 Çalışan 10 kanal listeye ekleniyor...\n")

    with requests.Session() as s:
        s.headers.update(headers)
        for base_url, kanallar in sunucu_verileri:
            for kalip in kanallar:
                # URL birleştirme (Eksik veya fazla / işaretini önler)
                test_url = f"{base_url}/{kalip}.m3u8"
                
                try:
                    # stream=True sunucunun dosyayı hemen onaylamasını sağlar
                    r = s.get(test_url, timeout=5, stream=True)
                    if r.status_code == 200:
                        # İsim düzenleme: nowtv/nowtv -> NOWTV
                        kanal_adi = kalip.split("/")[-1].replace("_1080p", "").replace("_720p", "").replace("_", " ").upper()
                        
                        yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{test_url}\n")
                        print(f"✅ AKTİF: {kanal_adi}")
                    r.close()
                except:
                    print(f"❌ BAĞLANTI HATASI: {kalip}")
                    continue

    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    
    print(f"\n✨ İşlem bitti! {len(yeni_liste)-1} kanal başarıyla dosyaya kaydedildi.")

if __name__ == "__main__":
    canli_kanal_hazirla()
