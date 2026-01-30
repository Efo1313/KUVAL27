import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def link_yakala():
    # GitHub Actions (Linux) uyumlu tarayıcı ayarları
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    print("Tarayıcı başlatılıyor...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://tr.mobiltv.net/trt-belgesel"
        driver.get(url)
        print("Sayfa yüklendi, link aranıyor (15 sn)...")
        time.sleep(15)

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
            m3u_content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik)\n{final_link}\n"
            
            with open("listem.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("✅ listem.m3u güncellendi.")
        else:
            print("❌ Link bulunamadı.")

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    link_yakala()
