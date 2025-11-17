import os
from ultralytics import YOLO

# Modeli hemen yükleme → önce yolu ayarla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

_model = None

def get_model():
    global _model
    if _model is None:
        _model = YOLO(MODEL_PATH)
    return _model


# 🟨 İngilizce → Türkçe etiket eşlemesi
etiket_cevir = {
    "carrot": "havuç",
    "apple": "elma",
    "banana": "muz",
    "orange": "portakal",
    "broccoli": "brokoli",
}


def gorsel_analiz(image_path):
    model = get_model()               # <-- Modeli burada yükle
    results = model(image_path)
    detected = set()

    for r in results:
        for c in r.boxes.cls:
            etiket = model.names[int(c)]
            detected.add(etiket_cevir.get(etiket, etiket))

    return list(detected)
