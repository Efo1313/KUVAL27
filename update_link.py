import requests
import re

def get_live_link():
    url = "https://m.canlitv.direct/atvcanli-yayin-izle"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://m.canlitv.direct/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        content = response.text

        # 1. Adım: Sayfa içinde doğrudan m3u8 linki ara
        # Bu genelde Player 1'dir.
        links = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', content)
        
        # 2. Adım: Eğer direkt link yoksa, iframe (Player seçenekleri) içinde ara
        if not links:
            # Sayfa içindeki diğer player linklerini (iframe src) bulalım
            player_frames = re.findall(r'iframe.*?src=["\'](.*?)["\']', content)
            for frame_url in player_frames:
                if not frame_url.startswith('http'):
                    frame_url = "https:" + frame_url if frame_url.startswith('//') else "https://m.canlitv.direct" + frame_url
                
                # Her bir player sayfasını tek tek ziyaret et
                f_res = requests.get(frame_url, headers=headers, timeout=10)
                f_links = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', f_res.text)
                if f_links:
                    links.extend(f_links)

        # Temizlik: Kaçış karakterlerini (\/) düzelt ve geçerli olanı seç
        if links:
            # İlk geçerli m3u8 linkini al ve temizle
            final_link = links[0].replace('\\/', '/')
            return final_link

    except Exception as e:
        print(f"Hata: {e}")
    return None

new_link = get_live_link()

with open("atv_listesi.m3u", "w", encoding="utf-8") as f:
    if new_link:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV Canlı\n{new_link}")
        print(f"Başarılı! Bulunan Link: {new_link}")
    else:
        f.write("#EXTM3U\n# Link bulunamadi. Playerlar taranmis olsa da site botu engelliyor.")
        print("Maalesef link bulunamadı.")
