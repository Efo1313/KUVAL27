import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ulusal_tara():
    veri = [
        {"sunucu": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo", "kanallar": ["atv/atv_1080p", "ahaber/ahaber_1080p", "aspor/aspor_1080p"]},
        {"sunucu": "https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba", "kanallar": ["kanald/kanald_1080p", "showtv/showtv_1080p"]},
        {"sunucu": "https://trthls.akamaized.net/hls/live", "kanallar": ["718012/trt1_1080p", "718013/trthaber_1080p", "718021/trtcocuk_1080p"]}
    ]
    yeni_liste = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    with requests.Session() as s:
        s.headers.update(headers)
        for grup in veri:
            for kalip in grup["kanallar"]:
                url = f"{grup['sunucu']}/{kalip}.m3u8"
                try:
                    if s.get(url, timeout=5, verify=False, stream=True).status_code == 200:
                        isim = kalip.split("/")[-1].replace("_1080p", "").upper()
                        if "718012" in isim: isim = "TRT 1"
                        yeni_liste.append(f"#EXTINF:-1,{isim}\n{url}\n")
                except: continue
                
    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
    print("✅ canli_tv_listem.m3u olusturuldu.")

if __name__ == "__main__":
    ulusal_tara()
