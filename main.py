import datetime
import urllib.request
import re
import os
from playwright.sync_api import sync_playwright

def hava_durumu_cek(sehir):
    try:
        url = f"https://wttr.in/{sehir}?format=%C+%t&m"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            sonuc = response.read().decode('utf-8').strip()
            
            ceviriler = {
                "Partly cloudy": "Parçalı Bulutlu",
                "Light rain": "Hafif Yağmurlu",
                "Heavy rain": "Şiddetli Yağmurlu",
                "Thunderstorm": "Gök Gürültülü Fırtına",
                "Sunny": "Güneşli",
                "Clear": "Açık",
                "Cloudy": "Bulutlu",
                "Overcast": "Kapalı",
                "Rain": "Yağmurlu",
                "Snow": "Karlı",
                "Mist": "Puslu",
                "Fog": "Sisli"
            }
            
            for ing, tr in ceviriler.items():
                if ing.lower() in sonuc.lower():
                    sonuc = re.sub(ing, tr, sonuc, flags=re.IGNORECASE)
                    break
            return sonuc
    except Exception as e:
        return "Güncellenemedi"

def panel_guncelle():
    # Türkiye saatine göre (UTC+3) tarih ve saat
    simdi = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    tarih_str = f"{simdi.day} {aylar[simdi.month - 1]} {simdi.year}, {gunler[simdi.weekday()]}"
    saat_str = simdi.strftime("%H:%M")

    saraykoy_hava = hava_durumu_cek("Saraykoy")
    golhisar_hava = hava_durumu_cek("Golhisar")

    # Bozulma ihtimaline karşı HTML'i her seferinde sıfırdan tertemiz oluşturuyoruz
    html_icerik = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kindle Panel</title>
    <style>
        body {{
            background-color: #ffffff;
            color: #000000;
            font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
            margin: 0;
            padding: 30px;
            width: 800px;
            height: 1050px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .header {{
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            border-bottom: 4px solid #000000;
            padding-bottom: 15px;
        }}
        .date-box {{
            font-size: 20px;
            text-align: center;
            margin-top: 10px;
            padding-bottom: 10px;
            border-bottom: 2px dashed #000000;
        }}
        .weather-box {{
            margin-top: 20px;
            font-size: 26px;
            line-height: 1.8;
            padding: 15px 20px;
            border: 3px solid #000000;
            border-radius: 10px;
        }}
        .todo-section {{
            margin-top: 20px;
            border: 3px solid #000000;
            padding: 20px;
            border-radius: 10px;
        }}
        .todo-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            border-bottom: 2px solid #000000;
            padding-bottom: 8px;
        }}
        .todo-item {{
            margin-bottom: 12px;
            font-size: 22px;
        }}
        .footer {{
            font-size: 17px;
            border-top: 4px solid #000000;
            padding-top: 15px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div>
        <div class="header">
            Denizli / Sarayköy &bull; Burdur / Gölhisar
        </div>
        <div class="date-box">
            <b>Tarih:</b> {tarih_str} &nbsp;|&nbsp; <b>Son Güncelleme:</b> {saat_str}
        </div>
        
        <div class="weather-box">
            &bull; <b>Sarayköy:</b> {saraykoy_hava}<br>
            &bull; <b>Gölhisar:</b> {golhisar_hava}
        </div>

        <div class="todo-section">
            <div class="todo-title">Günlük Yapılacaklar</div>
            <div class="todo-item">[ &nbsp; ] Kitap oku</div>
            <div class="todo-item">[ &nbsp; ] Projeyi tamamla</div>
            <div class="todo-item">[ &nbsp; ] Mola ver</div>
        </div>
    </div>

    <div class="footer">
        <b>Anadolu kadim takvimi:</b> <i>Eski Ay (Küçülürken)</i> salça, bulgur, tarhana, turşu, kurutmalık, ekim-dikim ve saç kesimi vaktidir. <b>Yeni Ay (Büyürken)</b> ise bunlardan kaçınılıp yeni iş ve başlangıçlar yapılır.
        <hr style="border: 1px solid #000000; margin: 10px 0;">
        &bull; <b>ESKİ AY DÖNEMİ:</b> Kışlık erzak ve toprak işlemleri için en bereketli zamandır.<br>
        &bull; <b>YENİ AY:</b> Yeni adımlar ve projeler için uygundur.
    </div>
</body>
</html>"""

    with open("panel.html", "w", encoding="utf-8") as f:
        f.write(html_icerik)
    print("panel.html sıfırdan oluşturuldu!")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 800, 'height': 1050})
        page.set_content(html_icerik, wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path="screen.png", full_page=True)
        browser.close()
    print("screen.png başarıyla oluşturuldu!")

if __name__ == "__main__":
    panel_guncelle()
