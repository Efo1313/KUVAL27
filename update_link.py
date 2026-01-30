from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def link_yakala_ve_kaydet():
    # 1. Tarayıcı Ayarları (Arka planda gizli çalışır)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    # 2. Chrome Driver'ı Otomatik Kur ve Başlat
    print("Sistem hazırlanıyor, lütfen bekleyin...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 3. Hedef Siteye Git
        url = "https://tr.mobiltv.net/trt-belgesel"
        print(f"Bağlanılıyor: {url}")
        driver.get(url)

        # Videonun yüklenmesi ve token oluşması için bekleme süresi
        print("Kanal linki yakalanıyor (15 saniye bekleyiniz)...")
        time.sleep(15)

        # 4. Ağ Trafiğini (Network Logs) İncele
        logs = driver.get_log('performance')
        found_links = []

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if 'Network.request' in log['method']:
                request_url = log['params'].get('request', {}).get('url', '')
                # M3U8 uzantılı ve içinde güvenlik tokeni olan linki filtrele
                if '.m3u8' in request_url and 'tkn=' in request_url:
                    found_links.append(request_url)

        # 5. M3U Dosyası Oluşturma
        if found_links:
            # En güncel ve benzersiz linki al
            final_link = list(set(found_links))[0]
            
            m3u_dosya_icerigi = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik)\n{final_link}\n"
            
            with open("listem.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_dosya_icerigi)
            
            print("\n" + "="*30)
            print("✅ BAŞARILI!")
            print(f"Dosya Adı: listem.m3u")
            print(f"Yeni Link: {final_link[:50]}...") # Linkin başını göster
            print("="*30)
        else:
            print("\n❌ HATA: Link yakalanamadı. Site link yapısını değiştirmiş olabilir veya internet yavaş kalmış olabilir.")

    except Exception as e:
        print(f"\nBir hata oluştu: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    link_yakala_ve_kaydet()
