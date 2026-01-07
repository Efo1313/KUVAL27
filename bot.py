import requests
import re

# Kanallar ve sayfaları (Daha kolay çekilebilen kaynaklar eklendi)
kanallar = {
    "Haberturk": "https://www.canlitv.com/haberturk-izle",
    "Show TV": "https://www.canlitv.com/show-tv-canli-izle-1",
    "ATV": "https://www.canlitv.com/atv-canli-izle",
    "Star TV": "https://www.canlitv.com/star-tv-canli-izle",
    "TRT Haber": "https://tv-trthaber.live.trt.com.tr/master.m3u8",
    "Halk TV": "https://www.youtube.com/watch?v=fXvI-MvL-fI"
}

def linki_yakala(name, url):
    if ".m3u8" in url or "youtube.com" in url:
        return url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.canlitv.com/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # m3u8 linklerini bulmak için gelişmiş tarama
        match = re.search(r'(https?://[^\s"\'<>]+(?:\.m3u8)[^\s"\'<>]*|https?://[^\s"\'<>]+playlist[^\s"\'<>]*|https?://[^\s"\'<>]+stream[^\s"\'<>]*)', response.text)
        
        if match:
            link = match.group(0).replace("\\/", "/")
            # Bazı siteler linki // ile başlatır, onu düzeltelim
            if link.startswith("//"):
                link = "https:" + link
            return link
    except:
        return None
    return None

with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for isim, adres in kanallar.items():
        yayin = linki_yakala(isim, adres)
        if yayin:
            f.write(f"#EXTINF:-1,{isim}\n{yayin}\n")

print("Yeni liste hazırlandı!")
