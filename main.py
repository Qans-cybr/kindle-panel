import datetime
import urllib.request
import re
from PIL import Image, ImageDraw, ImageFont

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
                "Thunderstorm": "Fırtınalı",
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
    except:
        return "Güncellenemedi"

def panel_olustur():
    simdi = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    tarih_str = f"{simdi.day} {aylar[simdi.month - 1]} {simdi.year}, {gunler[simdi.weekday()]}"
    saat_str = simdi.strftime("%H:%M")

    saraykoy = hava_durumu_cek("Saraykoy")
    golhisar = hava_durumu_cek("Golhisar")

    # 800x1050 boyutunda bembeyaz bir tuval oluştur
    img = Image.new('RGB', (800, 1050), color='white')
    draw = ImageDraw.Draw(img)

    # Ubuntu'daki standart Türkçe destekli fontları yükle
    font_yol_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_yol_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    f_baslik = ImageFont.truetype(font_yol_bold, 28)
    f_altbaslik = ImageFont.truetype(font_yol_bold, 24)
    f_normal = ImageFont.truetype(font_yol_reg, 22)
    f_kucuk_bold = ImageFont.truetype(font_yol_bold, 18)
    f_kucuk = ImageFont.truetype(font_yol_reg, 17)

    # 1. Üst Başlık
    draw.text((80, 35), "Denizli / Sarayköy  •  Burdur / Gölhisar", font=f_baslik, fill="black")
    draw.line([(30, 85), (770, 85)], fill="black", width=4)

    # 2. Tarih ve Saat
    draw.text((110, 105), f"Tarih: {tarih_str}   |   Saat: {saat_str}", font=f_normal, fill="black")
    draw.line([(30, 150), (770, 150)], fill="black", width=2)

    # 3. Hava Durumu Kutusu
    draw.rectangle([(30, 180), (770, 330)], outline="black", width=3)
    draw.text((55, 200), f"• Sarayköy :  {saraykoy}", font=f_altbaslik, fill="black")
    draw.text((55, 260), f"• Gölhisar  :  {golhisar}", font=f_altbaslik, fill="black")

    # 4. Yapılacaklar Listesi Kutusu
    draw.rectangle([(30, 360), (770, 680)], outline="black", width=3)
    draw.text((55, 385), "☑ Günlük Yapılacaklar", font=f_altbaslik, fill="black")
    draw.line([(55, 425), (745, 425)], fill="black", width=2)
    
    draw.text((65, 450), "☐  Kitap oku", font=f_normal, fill="black")
    draw.text((65, 505), "☐  Projeyi tamamla", font=f_normal, fill="black")
    draw.text((65, 560), "☐  Mola ver", font=f_normal, fill="black")
    draw.text((65, 615), "☐  Günlük tekrar ve hazırlık", font=f_normal, fill="black")

    # 5. Alt Bilgi - Anadolu Kadim Takvimi
    draw.line([(30, 830), (770, 830)], fill="black", width=4)
    draw.text((30, 850), "Anadolu Kadim Takvimi:", font=f_kucuk_bold, fill="black")
    draw.text((30, 880), "• Eski Ay (Küçülürken): Salça, bulgur, tarhana, turşu, kurutmalık,", font=f_kucuk, fill="black")
    draw.text((45, 905), "ekim-dikim ve saç kesimi için en bereketli ve dayanıklı zamandır.", font=f_kucuk, fill="black")
    draw.text((30, 945), "• Yeni Ay (Büyürken): Erzak işlerinden kaçınılır; yeni iş, adım ve", font=f_kucuk, fill="black")
    draw.text((45, 970), "projelere başlangıç yapmak için uygundur.", font=f_kucuk, fill="black")

    # Resmi kaydet
    img.save("screen.png")
    print("screen.png doğrudan çizilerek başarıyla oluşturuldu!")

if __name__ == "__main__":
    panel_olustur()
