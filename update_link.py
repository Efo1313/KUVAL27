import requests
import re

# Siteye gerçek bir tarayıcı gibi görünmek için başlık ekliyoruz
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

target_url = "https://m.canlitv.direct/atvcanli-yayin-izle"

def get_live_link():
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        # Linki bulmak için daha geniş bir arama
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Hata: {e}")
    return None

new_link = get_live_link()

if new_link:
    # Karakter temizliği (varsa kaçış karakterlerini düzeltir)
    new_link = new_link.replace('\\/', '/')
    with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canlı\n{new_link}")
    print(f"Link bulundu ve kaydedildi: {new_link}")
else:
    # Hata almamak için link bulunmasa bile boş bir dosya oluştururuz
    with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n# Link su an bulunamadi.")
    print("Link bulunamadı, boş dosya oluşturuldu.")
