from fastapi import FastAPI, Query
import json

app = FastAPI(title="KaloriBot API 🔥")

# 📂 Kalori verilerini yükle
with open("kalori_verisi.json", "r", encoding="utf-8") as f:
    kalori_data = json.load(f)

# 🔍 Kalori arama fonksiyonu
def kaloribot_sor(soru: str, limit: int = 10):
    soru = soru.lower().strip()

    # Türkçedeki ekleri basitçe temizle
    def temizle(kelime):
        ekler = ["nın", "nin", "nun", "nün", "in", "ın", "un", "ün", "ın", "in"]
        for ek in ekler:
            if kelime.endswith(ek) and len(kelime) > len(ek) + 2:
                return kelime[:-len(ek)]
        return kelime

    # Stopword'leri de temizleyelim
    anlamsizlar = {"kalori", "kalorisi", "kaç", "nedir", "ne", "kadar"}

    # 🔸 Soru kelimeleri temizleniyor
    kelimeler = [temizle(k) for k in soru.split() if k not in anlamsizlar]
    temiz_soru = " ".join(kelimeler)

    direkt_eslesenler = []
    parcali_eslesenler = []

    for item in kalori_data:
        orijinal_isim = item.get("isim", "").strip()
        isim = orijinal_isim.lower()
        isim_kelimeleri = [temizle(k) for k in isim.split()]
        temiz_isim = " ".join(isim_kelimeleri)

        # 🔥 Tam eşleşme kontrolü (temizlenmiş haliyle)
        if temiz_soru == temiz_isim:
            cumle = f"{orijinal_isim} ({item['birim']}) {item['kalori']} kaloridir."
            direkt_eslesenler.append(cumle)

        # 🔥 Parça eşleşme kontrolü
        elif any(k in temiz_isim for k in kelimeler):
            cumle = f"{orijinal_isim} ({item['birim']}) {item['kalori']} kaloridir."
            parcali_eslesenler.append(cumle)

    if direkt_eslesenler:
        return {"cevaplar": direkt_eslesenler}

    if parcali_eslesenler:
        return {"cevaplar": parcali_eslesenler[:limit]}

    return {"cevap": "Kalori bilgisi bulunamadı, farklı bir yemek adı deneyebilirsin."}


# 🔌 API endpoint
@app.get("/kalori/")
def kalori_sorgula(
    soru: str = Query(..., description="Kalorisini öğrenmek istediğin şey"),
    limit: int = Query(10, description="Maksimum kaç sonuç dönsün?")
):
    cevap = kaloribot_sor(soru, limit)
    if cevap:
        return cevap
    return {"cevap": "Bu kaloriyle ilgili bir soru değil gibi görünüyor."}