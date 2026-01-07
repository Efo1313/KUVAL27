import requests
import re

# Kanallar ve kaynaklar
kanallar = {
    "Haberturk": "https://tv.canlitvvolo.com/haberturk-tv-hd-izlee/",
    "ShowTV": "https://tv.canlitvvolo.com/show-tv-hd-izlee/",
    "Halk TV (YouTube)": "https://www.youtube.com/watch?v=fXvI-MvL-fI",
    "TRT Haber (Resmi)": "https://tv-trthaber.live.trt.com.tr/master.m3u8"
}

def linki_yakala(name, url):
    # Eğer link zaten m3u8 ise direkt döndür (TRT örneği gibi)
    if ".m3u8" in url:
        return url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://google.com'
    }
    
    try:
        # YouTube için özel kontrol (Basit yöntem)
        if "youtube.com" in url:
            return url # YouTube linkini direkt listeye ekle, player'lar genelde çözer
            
        response = requests.get(url, headers=headers, timeout=20)
        # Sitenin içindeki gizli m3u8 linkini daha geniş bir taramayla ara
        match = re.search(r'(https?://[^\s"\'<>]+(?:\.m3u8)[^\s"\'<>]*|https?://[^\s"\'<>]+playlist[^\s"\'<>]*|https?://[^\s"\'<>]+stream[^\s"\'<>]*)', response.text)
        
        if match:
            return match.group(0).replace("\\/", "/")
    except:
        return None
    return None

# M3U Dosyası Oluşturma
with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for isim, adres in kanallar.items():
        yayin = linki_yakala(isim, adres)
        if yayin:
            f.write(f"#EXTINF:-1,{isim}\n{yayin}\n")

print("İşlem tamam!")
