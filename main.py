import datetime
import urllib.request
import re
import os
from playwright.sync_api import sync_playwright

def hava_durumu_cek(sehir):
    try:
        url = f"https://wttr.in/{sehir}?format=%C+%t&m"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            sonuc = response.read().decode('utf-8').strip()
            
            ceviriler = {
                "Sunny": "Güneşli",
                "Clear": "Açık",
                "Partly cloudy": "Parçalı Bulutlu",
                "Cloudy": "Bulutlu",
                "Overcast": "Kapalı",
                "Light rain": "Hafif Yağmurlu",
                "Rain": "Yağmurlu",
                "Heavy rain": "Şiddetli Yağmurlu",
                "Thunderstorm": "Gök Gürültülü Fırtına",
                "Snow": "Karlı",
                "Mist": "Puslu",
                "Fog": "Sisli"
            }
            
            for ing, tr in ceviriler.items():
                if ing.lower() in sonuc.lower():
                    sonuc = re.sub(ing, tr, sonuc, flags=re.IGNORECASE)
                    
            return sonuc
    except:
        return "Bilgi alınamadı"

def panel_guncelle():
    simdi = datetime.datetime.now()
    
    saraykoy_hava = hava_durumu_cek("Saraykoy")
    golhisar_hava = hava_durumu_cek("Golhisar")

    print(f"Sarayköy Hava: {saraykoy_hava}")
    print(f"Gölhisar Hava: {golhisar_hava}")

    try:
        with open("panel.html", "r", encoding="utf-8") as f:
            html = f.read()

        hava_html = f'''<div class="weather-sub">
          &bull; <b>Sarayk&ouml;y:</b> {saraykoy_hava}<br>
          &bull; <b>G&ouml;lhisar:</b> {golhisar_hava}
        </div>'''
        
        html = re.sub(r'<div class="weather-sub">.*?<\/div>', hava_html, html, flags=re.DOTALL)

        with open("panel.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("panel.html başarıyla güncellendi!")

        # Ekran koruyucu görselini oluştururken sayfanın tam yüklenmesini bekle
        print("Ekran koruyucu görseli (`screen.png`) oluşturuluyor...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 800, 'height': 1050})
            path = os.path.abspath("panel.html")
            page.goto(f"file://{path}", wait_until="networkidle")
            page.screenshot(path="screen.png")
            browser.close()
        print("screen.png başarıyla oluşturuldu!")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    panel_guncelle()
