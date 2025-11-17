from fastapi import FastAPI, UploadFile, File, Form
from yolov8_analyzer import gorsel_analiz
from recipe_utils import tarif_bul, recipes
from chatbot import analiz_et  # Bunu ekledik!
from fastapi import Query
import json
from fastapi.middleware.cors import CORSMiddleware


import random

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya sadece frontend: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/soru")
async def soruya_cevap(soru: str = Form(...)):
    cevaplar = analiz_et(soru)

    # Rastgele istenirse
    if cevaplar == ["rastgele"]:
        rastgele = random.choice(recipes)
        return {
            "girdi": soru,
            "oneriler": [(rastgele["Name"], 0, rastgele["RecipeDetails"])]
        }

    return {"girdi": soru, "oneriler": cevaplar}

@app.post("/api/foto")
async def foto_ile_cevap(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    # YOLO ile malzeme tespiti
    malzemeler = gorsel_analiz(path)

    # Tarifleri bul (zaten detaylı formatta dönüyor)
    tarifler = tarif_bul(malzemeler)

    return {
        "tespit_edilen_malzemeler": malzemeler,  # 🧠 Bunu ekledik!
        "oneriler": tarifler
    }

# JSON verisini yükle (bir kere yükle yeter)
with open("kalori_verisi.json", "r", encoding="utf-8") as f:
    kalori_data = json.load(f)

def kaloribot_sor(soru: str, limit: int = 10):
    soru = soru.lower().strip()

    def temizle(kelime):
        ekler = ["nın", "nin", "nun", "nün", "in", "ın", "un", "ün"]
        for ek in ekler:
            if kelime.endswith(ek) and len(kelime) > len(ek) + 2:
                return kelime[:-len(ek)]
        return kelime

    anlamsizlar = {"kalori", "kalorisi", "kaç", "nedir", "ne", "kadar"}
    kelimeler = [temizle(k) for k in soru.split() if k not in anlamsizlar]
    temiz_soru = " ".join(kelimeler)

    direkt_eslesenler = []
    parcali_eslesenler = []

    for item in kalori_data:
        orijinal_isim = item.get("isim", "").strip()
        isim = orijinal_isim.lower()
        isim_kelimeleri = [temizle(k) for k in isim.split()]
        temiz_isim = " ".join(isim_kelimeleri)

        if temiz_soru == temiz_isim:
            cumle = f"{orijinal_isim} ({item['birim']}) {item['kalori']} kaloridir."
            direkt_eslesenler.append(cumle)
        elif any(k in temiz_isim for k in kelimeler):
            cumle = f"{orijinal_isim} ({item['birim']}) {item['kalori']} kaloridir."
            parcali_eslesenler.append(cumle)

    if direkt_eslesenler:
        return {"cevaplar": direkt_eslesenler}
    if parcali_eslesenler:
        return {"cevaplar": parcali_eslesenler[:limit]}
    return {"cevap": "Kalori bilgisi bulunamadı, farklı bir yemek adı deneyebilirsin."}

@app.get("/kalori/")
def kalori_sorgula(
    soru: str = Query(..., description="Kalorisini öğrenmek istediğin şey"),
    limit: int = Query(10, description="Maksimum kaç sonuç dönsün?")
):
    cevap = kaloribot_sor(soru, limit)
    if cevap:
        return cevap
    return {"cevap": "Bu kaloriyle ilgili bir soru değil gibi görünüyor."}