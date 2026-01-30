import cloudscraper
import re
import os

def get_atv_live_link():
    # Cloudflare ve bot korumalarını aşmak için scraper oluştur
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    
    # En güncel çalışan alternatif sayfalar
    urls = [
        "https://m.canlitv.direct/atv-canli-yayin-izle",
        "https://www.canlitv.me/atv-canli-izle-1",
        "https://canlitv.center/atv-canli-yayin"
    ]

    # m3u8 yakalama paterni (Kaçış karakterlerini de kapsar)
    pattern = r'(https?[:\\]+[^"\']+\.m3u8[^"\']*)'

    print("--- Canlı Yayın Linki Aranıyor ---")

    for url in urls:
        try:
            print(f"Sorgulanıyor: {url}")
            response = scraper.get(url, timeout=15)
            
            if response.status_code == 200:
                # Sayfa içeriğindeki tüm m3u8 linklerini bul
                matches = re.findall(pattern, response.text)
                
                for link in matches:
                    # Linki temizle
                    clean_link = link.replace('\\/', '/')
                    
                    # 'atv' kelimesi geçen ve 'daioncdn' barındıran linki önceliklendir
                    if "atv" in clean_link.lower() and "m3u8" in clean_link:
                        # Gereksiz tırnak veya karakter varsa temizle
                        clean_link = clean_link.strip('\\"\'')
                        print(f"✅ Başarılı! Aktif yayın bulundu.")
                        return clean_link
        except Exception as e:
            print(f"❌ Hata oluştu: {url} -> {e}")
            continue

    return None

# --- Dosyaya Yazma İşlemi ---
new_link = get_atv_live_link()
file_name = "atv_guncel.m3u"

with open(file_name, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if new_link:
        f.write(f"#EXTINF:-1,ATV Canli (Guncel)\n{new_link}")
        print(f"\nSonuç: {file_name} dosyası güncellendi.")
        print(f"Bulunan Link: {new_link}")
    else:
        # Hiçbiri olmazsa son çare:
        fallback = "https://atv-live.daioncdn.net/atv/atv.m3u8"
        f.write(f"#EXTINF:-1,ATV (Yedek)\n{fallback}")
        print("\n⚠️ Canlı link ayıklanamadı. Bot koruması çok güçlü olabilir.")
