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
    # Sitenin bot algılamasını zorlaştıran en kritik ayar:
    chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1")
    
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    print("--- Hedef Siteden Veri Çekme Başlatıldı ---")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Siteye doğrudan kanal linki üzerinden gidiyoruz
        url = "https://tr.mobiltv.net/trt-belgesel"
        driver.get(url)
        
        # Sitenin yüklenmesi için beklerken sayfayı hafifçe kaydıralım
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 200);")
        print("Sayfa aktif, linkler taranıyor...")
        time.sleep(20) 

        logs = driver.get_log('performance')
        found_links = []

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if 'Network.request' in log['method']:
                request_url = log['params'].get('request', {}).get('url', '')
                # Sitenin kullandığı m3u8 formatını yakala
                if '.m3u8' in request_url:
                    # Bazı siteler statik m3u8 kullanır, bazıları tokenlı
                    found_links.append(request_url)

        if found_links:
            # En uzun link genelde gerçek yayın linkidir (tokenlar nedeniyle)
            final_link = max(found_links, key=len)
            print(f"✅ Link Yakalandı!")
            content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (MobilTV)\n{final_link}\n"
        else:
            # Link bulunamazsa dosyayı bozma, ne hata olduğunu yaz
            print("❌ Link bulunamadı. Site koruması aşılamadı.")
            content = "#EXTM3U\n# Link su an yakalanamadi, site erisimi reddetti.\n"

        with open("listem.m3u", "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        print(f"❗ Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    link_yakala()
