import requests
import re
import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://m.canlitv.direct/"
}

target_url = "https://m.canlitv.direct/atvcanli-yayin-izle"

def get_live_link():
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        content = response.text
        
        # 1. Yöntem: Standart m3u8 arama
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', content)
        
        # 2. Yöntem: Eğer link HTML entity şeklinde gizlendiyse (unquote)
        if not match:
            content = html.unescape(content)
            match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', content)

        if match:
            link = match.group(1).replace('\\/', '/')
            return link
            
    except Exception as e:
        print(f"Hata: {e}")
    return None

new_link = get_live_link()

with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    if new_link:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canlı\n{new_link}")
        print(f"Başarılı! Link bulundu: {new_link}")
    else:
        # Eğer hala bulunamadıysa, manuel kontrol için site içeriğinin bir kısmını loglayalım
        f.write("#EXTM3U\n# Link su an bulunamadi.")
        print("Maalesef link hala bulunamadı. Site yapısı korunuyor olabilir.")
