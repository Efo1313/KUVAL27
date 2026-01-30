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
    # Gerçek bir kullanıcı gibi görünmek için User-Agent ekliyoruz
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    print("Tarayıcı başlatılıyor...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://tr.mobiltv.net/trt-belgesel"
        print(f"Siteye gidiliyor: {url}")
        driver.get(url)
        
        # Sayfanın tamamen oturması ve JS'lerin çalışması için bekleme
        print("Sayfa yükleniyor, 30 saniye bekleniyor...")
        time.sleep(30) 

        # Sayfa kaynağını kontrol et (Loglarda ne olduğunu görmek için)
        print(f"Sayfa başlığı: {driver.title}")

        logs = driver.get_log('performance')
        found_links = []

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if 'Network.request' in log['method']:
                request_url = log['params'].get('request', {}).get('url', '')
                if '.m3u8' in request_url and 'tkn=' in request_url:
                    found_links.append(request_url)

        if found_links:
            final_link = list(set(found_links))[0]
            print(f"✅ Başarılı! Link bulundu: {final_link[:50]}...")
            
            m3u_content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik)\n{final_link}\n"
            
            with open("listem.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            # Hata durumunda boş dosya oluşturma ki Actions çökmesin, 
            # ama loglarda neden olmadığını anlayalım
            print("❌ HATA: M3U8 linki yakalanamadı!")
            # Debug için sayfa içeriğinin bir kısmını yazdırabiliriz
            # print(driver.page_source[:500]) 

    except Exception as e:
        print(f"❗ Kritik Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    link_yakala()
