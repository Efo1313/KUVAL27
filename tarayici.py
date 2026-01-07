import requests

def ana_liste():
    yeni_liste = ["#EXTM3U\n"]
    # Senin bildiğin sağlam çalışan linkler
    kanallar = [
        {"isim": "ATV HD (1080p)", "url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8"},
        {"isim": "A Haber HD", "url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/ahaber/ahaber_1080p.m3u8"},
        {"isim": "A Spor HD", "url": "http://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor_1080p.m3u8"}
    ]
    
    for k in kanallar:
        yeni_liste.append(f"#EXTINF:-1,{k['isim']}\n{k['url']}\n")

    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)

if __name__ == "__main__":
    ana_liste()
