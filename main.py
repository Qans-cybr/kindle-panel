import datetime
import urllib.request
import re
import os
from playwright.sync_api import sync_playwright

def hava_durumu_cek(sehir):
    try:
        url = f"https://wttr.in/{sehir}?format=%C+%t"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except:
        return "Bilgi alınamadı"

def panel_guncelle():
    simdi = datetime.datetime.now()
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    gun_adi = gunler[simdi.weekday()]
    ay_adi = aylar[simdi.month - 1]
    tarih_str = f"{simdi.day} {ay_adi} {gun_adi}"
    saat_str = simdi.strftime("%H:%M")

    saraykoy_hava = hava_durumu_cek("Saraykoy")
    golhisar_hava = hava_durumu_cek("Golhisar")

    print(f"Tarih: {tarih_str} {saat_str}")
    print(f"Sarayköy Hava: {saraykoy_hava}")
    print(f"Gölhisar Hava: {golhisar_hava}")

    try:
        with open("panel.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Tarih ve saat güncelleme
        html = re.sub(r'<b>Saat:<\/b>.*?&nbsp;', f'<b>Saat:</b> {saat_str} &nbsp;', html)
        html = re.sub(r'<b>Tarih:<\/b>.*?<\/div>', f'<b>Tarih:</b> {tarih_str}</div>', html, flags=re.DOTALL)

        # Hava durumlarını güncelleme
        hava_html = f'<div class="weather-sub">\n        &bull; <b>Sarayk&ouml;y:</b> {saraykoy_hava}<br>\n        &bull; <b>G&ouml;lhisar:</b> {golhisar_hava}\n      </div>'
        html = re.sub(r'<div class="weather-sub">.*?<\/div>', hava_html, html, flags=re.DOTALL)

        with open("panel.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("panel.html başarıyla güncellendi!")

        # HTML dosyasını Kindle ekran ölçülerine uygun PNG görseline çevir
        print("Ekran koruyucu görseli (`screen.png`) oluşturuluyor...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # Kindle e-ink ekran boyutlarına uygun oran (örneğin 800x1000)
            page = browser.new_page(viewport={'width': 800, 'height': 1050})
            path = os.path.abspath("panel.html")
            page.goto(f"file://{path}")
            page.screenshot(path="screen.png")
            browser.close()
        print("screen.png başarıyla oluşturuldu!")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    panel_guncelle()
