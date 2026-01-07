import requests

def kanal_listesini_hazirla():
    # Dünya çapındaki güvenilir IPTV veritabanı (Türkiye kanalları)
    kaynak_url = "https://iptv-org.github.io/iptv/countries/tr.m3u"
    
    # Senin listene eklemek istediğin özel kanalların isimleri
    istenen_kanallar = ["Haberturk", "Show TV", "ATV", "Star TV", "Kanal D", "FOX", "TV8", "TRT 1", "TRT Haber", "A Haber", "Bloomberg HT"]
    
    try:
        response = requests.get(kaynak_url, timeout=20)
        satirlar = response.text.split('\n')
        
        yeni_liste = ["#EXTM3U\n"]
        
        # Veritabanını tara ve istediğimiz kanalları bul
        for i in range(len(satirlar)):
            if "#EXTINF" in satirlar[i]:
                for kanal in istenen_kanallar:
                    if kanal.lower() in satirlar[i].lower():
                        yeni_liste.append(satirlar[i] + "\n") # Kanal bilgisi
                        yeni_liste.append(satirlar[i+1] + "\n") # Yayın linki
                        break
        
        # YouTube yedeğini de manuel ekleyelim
        yeni_liste.append("#EXTINF:-1,Halk TV (YouTube)\nhttps://www.youtube.com/watch?v=fXvI-MvL-fI\n")

        # Dosyayı kaydet
        with open("canli_tv_listem.m3u", "w", encoding="utf-8") as f:
            f.writelines(yeni_liste)
            
        print("Liste dev veritabanından başarıyla güncellendi!")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    kanal_listesini_hazirla()
