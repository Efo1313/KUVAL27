import requests
import re

def liste_olustur():
    base_url = "http://5.178.103.239:82/yt1/s/"
    yeni_liste = ["#EXTM3U\n"]
    
    try:
        # Sunucuyu tara
        response = requests.get(base_url, timeout=15)
        dosyalar = re.findall(r'href="([^"]+\.m3u8)"', response.text)
        
        # Alfabetik sırala ve temizle
        benzersiz_dosyalar = sorted(list(set(dosyalar)))
        
        for dosya in benzersiz_dosyalar:
            # Geçici dosyaları atla
            if ".tmp" in dosya or ".." in dosya:
                continue
            
            # Kanal adını senin istediğin formatta yap (Baş harfler büyük)
            kanal_adi = dosya.replace(".m3u8", "").replace("_", " ").title()
            tam_link = base_url + dosya
            yeni_liste.append(f"#EXTINF:-1,{kanal_adi}\n{tam_link}\n")
            
        print(f"{len(yeni_liste)-1} kanal listeye eklendi.")

    except Exception as e:
        print(f"Hata: {e}")

    # Sildiğin dosyaları BURADA isim olarak belirtiyoruz ki bot onları geri getirsin
    hedef_dosyalar = [
        "Ozel_sunucu.m3u",
        "canli_tv_listem.m3u",
        "tam_kanal_listesi.m3u",
        "guncel_kanallarim.m3u"
    ]

    for dosya_adi in hedef_dosyalar:
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.writelines(yeni_liste)
        print(f"Oluşturuldu: {dosya_adi}")

if __name__ == "__main__":
    liste_olustur()
