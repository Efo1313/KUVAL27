import requests
import re

def get_live_link():
    base_url = "https://m.canlitv.direct/atvcanli-yayin-izle"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://m.canlitv.direct/"
    }

    try:
        # 1. ADIM: Ana sayfaya girip 'security' anahtarını yakala
        response = requests.get(base_url, headers=headers, timeout=15)
        # geolive.php?kanal=atvcanli-yayin-izle&security=XXXXX yapısını bul
        geo_match = re.search(r'geolive\.php\?kanal=atvcanli-yayin-izle&amp;security=([a-z0-9]+)', response.text)
        
        if not geo_match:
            print("Güvenlik anahtarı bulunamadı.")
            return None
        
        security_token = geo_match.group(1)
        player_url = f"https://m.canlitv.direct/geolive.php?kanal=atvcanli-yayin-izle&security={security_token}"
        
        # 2. ADIM: Player sayfasına git (Yayın linki burada saklı)
        player_response = requests.get(player_url, headers=headers, timeout=15)
        
        # 3. ADIM: Sayfa içindeki gerçek m3u8 linkini ayıkla
        # Genellikle 'source: "http..."' veya 'file: "http..."' içindedir
        m3u8_links = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', player_response.text)
        
        if m3u8_links:
            # En temiz linki al ve ters bölü işaretlerini düzelt
            clean_link = m3u8_links[0].replace('\\/', '/')
            return clean_link

    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

# M3U Dosyasını Yazdır
new_link = get_live_link()

with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    if new_link:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canlı\n{new_link}")
        print(f"Başarılı! Link: {new_link}")
    else:
        f.write("#EXTM3U\n# Yayina ulasilamadi. Site korumasi aktif.")
        print("Link bulunamadı.")
