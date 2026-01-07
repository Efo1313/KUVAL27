import requests
import re

def sunucu_tara():
    # Tarama yapılacak klasör adresi
    target_url = "http://5.178.103.239:82/yt1/s/"
    output_file = "ozel_sunucu_listesi.m3u"
    
    print(f"{target_url} adresi taranıyor...")
    
    try:
        # Sunucuya bağlanmayı dene
        response = requests.get(target_url, timeout=15)
        
        if response.status_code == 200:
            # Sayfa içindeki tüm .m3u8 linklerini bul
            linkler = re.findall(r'href="([^"]+\.m3u8)"', response.text)
            
            if linkler:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("#EXTM3U\n")
                    for link in linkler:
                        # Linki temizle ve tam hale getir
                        temiz_link = target_url + link
                        kanal_adi = link.replace(".m3u8", "").replace("_", " ").upper()
                        f.write(f"#EXTINF:-1, [SUNUCU] {kanal_adi}\n{temiz_link}\n")
                print(f"Başarılı! {len(linkler)} kanal bulundu ve {output_file} dosyasına kaydedildi.")
            else:
                print("Sunucu açık ama içinde .m3u8 dosyası bulunamadı.")
        else:
            print(f"Sunucu hata verdi! Hata kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Bağlantı kurulamadı: {e}")

if __name__ == "__main__":
    sunucu_tara()
