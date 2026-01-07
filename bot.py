import requests
import re

# Çekmek istediğin siteleri buraya ekle
kanallar = {
    "Haberturk": "https://tv.canlitvvolo.com/haberturk-tv-hd-izlee/",
    "ShowTV": "https://tv.canlitvvolo.com/show-tv-hd-izlee/",
    "BloombergHT": "https://tv.canlitvvolo.com/bloomberg-ht-izle-hd/"
}

def linki_yakala(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # Siteye bağlanıyoruz
        response = requests.get(url, headers=headers, timeout=10)
        # Sayfanın içinde gizli olan .m3u8 linkini cımbızla çekiyoruz
        match = re.search(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
        if match:
            return match.group(0)
    except:
        return None
    return None

# M3U Dosyasını Oluşturma
with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for isim, adres in kanallar.items():
        yayin_linki = linki_yakala(adres)
        if yayin_linki:
            f.write(f"#EXTINF:-1,{isim}\n{yayin_linki}\n")
            print(f"Başarılı: {isim} linki alındı.")
        else:
            print(f"Hata: {isim} linki bulunamadı.")

print("Liste başarıyla hazırlandı!")

