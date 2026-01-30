from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

# 1. Tarayıcı Ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://tr.mobiltv.net/trt-belgesel"
print(f"{url} adresi taranıyor...")
driver.get(url)

time.sleep(10) # Linkin oluşması için bekleme

logs = driver.get_log('performance')
found_links = []

for entry in logs:
    log = json.loads(entry['message'])['message']
    if 'Network.request' in log['method']:
        request_url = log['params'].get('request', {}).get('url', '')
        if '.m3u8' in request_url and 'tkn=' in request_url:
            found_links.append(request_url)

driver.quit()

# --- M3U DOSYASINA YAZMA BÖLÜMÜ ---
if found_links:
    # Set kullanarak sadece benzersiz ve en güncel linki alıyoruz
    final_link = list(set(found_links))[0] 
    
    m3u_content = f"#EXTM3U\n#EXTINF:-1,TRT Belgesel (Otomatik Güncel)\n{final_link}\n"
    
    with open("listem.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("\n✅ Link başarıyla yakalandı ve 'listem.m3u' dosyasına kaydedildi!")
    print(f"Güncel Link: {final_link}")
else:
    print("❌ Maalesef link bulunamadı.")
