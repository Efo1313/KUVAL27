import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def link_yakala():
    # 1. GitHub Actions (Ubuntu) İçin Optimize Edilmiş Tarayıcı Ayarları
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ekran olmadan çalış
    chrome_options.add_argument("--no-sandbox") # Güvenlik duvarını devre dışı bırak (Linux için şart)
    chrome_options.add_argument("--disable-dev-shm-usage") # Bellek hatalarını önle
    chrome_options.add_argument("--disable-gpu")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    print("Tarayıcı hazırlanıyor...")
    
    try:
        # 2. WebDriver Kurulumu
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 3. Siteye Giriş
        url = "https://tr.mobiltv.net/trt-belgesel"
        print(f"Adrese gidiliyor: {url}")
        driver.get(url)
        
        # Sayfanın ve JS paketlerinin yüklenmesi için yeterli süre tanıyalım
        print("Link yakalanıyor (20 saniye bekleniyor)...")
        time.sleep(20)

        # 4. Network Loglarını Analiz Et
        logs = driver.get_log('performance')
        found_links = []

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if 'Network.request' in log['method']:
                request_url = log['params'].get('request', {}).get('url', '')
                # M3U8 uzantılı ve içinde token olan linki bul
                if '.m3u8' in request_url and 'tkn=' in request_url:
                    found_links.append(request_url)

        # 5. Dosya Oluşturma ve Kaydetme
        if found_links:
            # En son/güncel linki al
            final_link = list(set(found_links))[0]
            print(f"Başarılı! Link bulundu: {final_link[:60]}...")
            
            # İçeriği hazırla
            m3u_content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik)\n{final_link}\n"
            
            # Dosyayı ana dizine yaz
            filepath = os.path.join(os.getcwd(), "listem.m3u")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(m3u_content)
            
            print(f"✅ {filepath} dosyası güncellendi.")
        else:
            print("❌ HATA: M3U8 linki yakalanamadı. Bekleme süresini artırmayı deneyin.")

    except Exception as e:
        print(f"❗ Beklenmedik bir hata oluştu: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Tarayıcı kapatıldı.")

if __name__ == "__main__":
    link_yakala()
