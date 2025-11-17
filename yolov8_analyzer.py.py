from ultralytics import YOLO

model = YOLO("best.pt")

# 🟨 İngilizce → Türkçe etiket eşlemesi
etiket_cevir = {
    "carrot": "havuç",
    "apple": "elma",
    "banana": "muz",
    "orange": "portakal",
    "broccoli": "brokoli",
    # Gerekirse diğerlerini de ekleyebiliriz
}

def gorsel_analiz(image_path):
    results = model(image_path)
    detected = set()
    for r in results:
        for c in r.boxes.cls:
            etiket = model.names[int(c)]
            # Etiketi çevir varsa, yoksa olduğu gibi bırak
            detected.add(etiket_cevir.get(etiket, etiket))
    return list(detected)