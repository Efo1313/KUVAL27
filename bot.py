import requests
import re

def liste_olustur():
    base_url = "http://5.178.103.239:82/yt1/s/"
    yeni_liste = ["#EXTM3U\n"]
    
    try:
        # Sunucu dizinine bağlanıp içindeki dosyaları tarıyoruz
        response = requests.get(base_url, timeout=15)
        # Sayfa içindeki .m3u8 ile biten tüm linkleri yakalıyoruz
        dosyalar = re.findall(r'href="([^"]+\.m3u8)"', response.text)
        
        if dosyalar:
            for dosya in dosyalar:
                # Dosya adını kanal ismi yapalım (örn: kemalsunal1.m3u8 -> Kemal Sunal 1)
                kanal_adi = dosya.replace(".m3u8", "").replace("_", " ").title()
                tam_link = base_url + dosya
                yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{tam_link}\n")
            print(f"{len(dosyalar)} adet kanal bulundu ve eklendi.")
        else:
            # Eğer tarama başarısız olursa manuel ekleme yapalım
            yeni_liste.append(f"#EXTINF:-1,Kemal Sunal 1\n{base_url}kemalsunal1.m3u8\n")

    except Exception as e:
        print(f"Sunucu taranırken hata oluştu: {e}")

    # Dosyayı Kaydet
    with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)

if __name__ == "__main__":
    liste_olustur()
