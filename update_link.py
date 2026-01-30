import cloudscraper
import re
import sys

def get_atv_link():
    # Tarayıcı gibi davranan bir scraper oluştur
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    
    # Alternatif kaynak siteler
    urls = [
        "https://m.canlitv.direct/atv-canli-yayin-izle",
        "https://www.canlitv.me/atv-canli-izle-1",
        "https://canlitv.center/atv-canli-yayin"
    ]
    
    # m3u8 yakalamak için geliştirilmiş regex
    pattern = r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']'

    print("--- ATV Linki Aranıyor ---")

    for url in urls:
        try:
            print(f"Denetleniyor: {url}")
            response = scraper.get(url, timeout=20)
            
            if response.status_code == 200:
                # Sayfadaki tüm olası m3u8 linklerini bul
                matches = re.findall(pattern, response.text)
                for link in matches:
                    # Kaçış karakterlerini temizle
                    clean_link = link.replace('\\/', '/')
                    # Sadece içinde atv geçen geçerli linki al
                    if "atv" in clean_link.lower() and ".m3u8" in clean_link:
                        final_link = clean_link.strip('\\"\'')
                        print(f"✅ Başarılı: {final_link}")
                        return final_link
        except Exception as e:
            print(f"❌ Hata: {url} -> {e}")
            continue
            
    return None

# Dosya oluşturma ve yazma
new_link = get_atv_link()
output_file = "atv_listesi.m3u"

try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if new_link:
            f.write(f"#EXTINF:-1,ATV Canli\n{new_link}")
            print(f"İşlem tamam: {output_file} güncellendi.")
        else:
            # Token gerektiren ama ana omurga olan yedek link
            fallback = "https://atv-live.daioncdn.net/atv/atv.m3u8"
            f.write(f"#EXTINF:-1,ATV (Yedek)\n{fallback}")
            print("Uyarı: Canlı link bulunamadı, yedek link yazıldı.")
except Exception as e:
    print(f"Dosya yazma hatası: {e}")
    sys.exit(1)
