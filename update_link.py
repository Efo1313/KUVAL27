import requests
import re
import cloudscraper

def get_atv_from_site():
    # Sitenin bot korumasını aşmak için cloudscraper kullanıyoruz
    scraper = cloudscraper.create_scraper()
    
    # Senin verdiğin ana sayfa ve onun yayın yaptığı muhtemel alt yollar
    urls = [
        "https://m.canlitv.direct/atvcanli-yayin-izle",
        "https://m.canlitv.direct/yayin.php?kanal=atvcanli-yayin-izle"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://m.canlitv.direct/"
    }

    print("--- m.canlitv.direct Taraması Başlatıldı ---")

    for url in urls:
        try:
            response = scraper.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                # 1. Adım: HTML içinde doğrudan m3u8 ara
                # 2. Adım: Kaçış karakterli (\/) linkleri temizle
                content = response.text
                matches = re.findall(r'["\'](https?[:\\]+[^"\']+\.m3u8[^"\']*)["\']', content)
                
                for link in matches:
                    clean_link = link.replace('\\/', '/')
                    # Sadece atv içeren ve reklam olmayan linki seç
                    if "atv" in clean_link.lower() and "m3u8" in clean_link:
                        # Eğer link daioncdn ise genellikle token gerekir, 
                        # ama site üzerinden alınan linkte bu token zaten ekli olur.
                        print(f"✅ Link bulundu: {clean_link}")
                        return clean_link
        except Exception as e:
            print(f"Hata: {e}")
            continue

    # Eğer siteden çekemezse (Bulgaristan engeli varsa), global yedek mekanizmasını çalıştır
    print("⚠️ Siteden çekilemedi, global havuzlara bakılıyor...")
    backup_res = requests.get("https://iptv-org.github.io/iptv/countries/tr.m3u", timeout=10)
    if backup_res.status_code == 200:
        match = re.search(r'#EXTINF.*ATV.*\n(https?://.*\.m3u8.*)', backup_res.text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return "https://trkvz-live.ercdn.net/atv/atv.m3u8" # En son çare

# Yazma işlemi
new_link = get_atv_from_site()
with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"#EXTINF:-1,ATV Canli\n{new_link}")

print(f"İşlem Tamam. Kaydedilen link: {new_link}")
