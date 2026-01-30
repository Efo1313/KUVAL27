from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# 1. Tarayıcı Ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ekran açılmadan arka planda çalışır
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# 2. Driver'ı Başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 3. Hedef Siteye Git
url = "https://tr.mobiltv.net/trt-belgesel"
print(f"{url} adresi taranıyor...")
driver.get(url)

# Sayfanın ve videonun yüklenmesi için 10 saniye bekle
time.sleep(10)

# 4. Ağ Loglarını İncele
logs = driver.get_log('performance')

found_links = []
for entry in logs:
    log = json.loads(entry['message'])['message']
    if 'Network.request' in log['method']:
        request_url = log['params'].get('request', {}).get('url', '')
        # İçinde .m3u8 geçen ve token içeren linki yakala
        if '.m3u8' in request_url and 'tkn=' in request_url:
            found_links.append(request_url)

# 5. Sonuçları Yazdır
if found_links:
    print("\n--- Başarıyla Yakalanan Linkler ---")
    for link in set(found_links): # set() ile tekrar edenleri temizle
        print(link)
else:
    print("Maalesef link bulunamadı. Bekleme süresini artırmayı deneyin.")

driver.quit()
