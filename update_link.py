import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def link_yakala():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Gerçek kullanıcı taklidi
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    print("--- Tarayıcı Başlatılıyor ---")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://tr.mobiltv.net/trt-belgesel"
        print(f"Hedef Site: {url}")
        driver.get(url)
        
        # Sitenin yüklenmesi için 30 saniye sabırla bekle
        print("Sayfa yükleniyor (30 sn)...")
        time.sleep(30) 

        print(f"Giriş Yapılan Sayfa Başlığı: {driver.title}")
        print(f"Mevcut URL: {driver.current_url}")

        logs = driver.get_log('performance')
        found_links = []

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if 'Network.request' in log['method']:
                request_url = log['params'].get('request', {}).get('url', '')
                if '.m3u8' in request_url and 'tkn=' in request_url:
                    found_links.append(request_url)

        # DOSYA OLUŞTURMA GARANTİSİ
        # Eğer link varsa içine yaz, yoksa mevcut dosyayı koru veya boş oluştur
        if found_links:
            final_link = list(set(found_links))[0]
            print(f"✅ BAŞARILI: Link bulundu!")
            content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik)\n{final_link}\n"
        else:
            print("⚠️ UYARI: Link yakalanamadı! Site engellemiş veya yüklenmemiş olabilir.")
            # Hata almamak için dosyayı en azından eski haliyle veya boş bırakalım
            if os.path.exists("listem.m3u"):
                print("Eski dosya korunuyor.")
                return
            content = "#EXTM3U\n# Link Bulunamadi\n"

        with open("listem.m3u", "w", encoding="utf-8") as f:
            f.write(content)
            print("Dosya sisteme kaydedildi.")

    except Exception as e:
        print(f"❗ Hata Oluştu: {e}")
        # Hata olsa bile boş dosya oluştur ki Actions çökmesin
        if not os.path.exists("listem.m3u"):
            with open("listem.m3u", "w") as f: f.write("# Hata Olustu")
    finally:
        driver.quit()

if __name__ == "__main__":
    link_yakala()
