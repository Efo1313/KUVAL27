import requests
import re

# Kanal isimleri ve sayfa linkleri
kanallar = {
    "Haberturk": "https://tv.canlitvvolo.com/haberturk-tv-hd-izlee/",
    "ShowTV": "https://tv.canlitvvolo.com/show-tv-hd-izlee/",
    "BloombergHT": "https://tv.canlitvvolo.com/bloomberg-ht-izle-hd/",
    "Halk TV": "https://tv.canlitvvolo.com/halk-tv-hd-izle-canli/"
}

def linki_yakala(url):
    # Siteyi "Ben gerçek bir kullanıcıyım" diye kandırmak için başlıklar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://tv.canlitvvolo.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # Daha gelişmiş bir arama yöntemi (farklı tırnak tiplerini de kapsar)
        match = re.search(r'(https?://[^\s"\']+\.m3u8)', response.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None
    return None

# M3U Dosyasını Oluşturma
with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for isim, adres in kanallar.items():
        yayin_linki = linki_yakala(adres)
        if yayin_linki:
            f.write(f"#EXTINF:-1,{isim}\n{yayin_linki}\n")
            print(f"Başarılı: {isim}")
        else:
            # Eğer link bulunamazsa, sistemin çalıştığını anlaman için bir uyarı ekler
            print(f"Link bulunamadı: {isim}")

print("Dosya başarıyla güncellendi!")
