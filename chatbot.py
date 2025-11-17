import re
from recipe_utils import tarif_bul, tarif_bul_kategori
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords", quiet=True)
stopwords_tr = set(stopwords.words("turkish"))

# ➕ Fazladan anlam katmayan kelimeleri filtrele (sonradan) 10.05.2025
fiil_filtresi = {
    "yapabilirim", "hazırlayabilirim", "yapılır", "yapmak", "pişirmek", "pişer",
    "olur", "ne", "ile", "yapsam", "pişirsem", "yemek", "acaba", "nasıl",
    "bir", "şey", "şöyle", "neden", "olsun", "isterim", "bugün", "canım"
}


def analiz_et(soru):
    soru = soru.lower()

    if "bugün" in soru and ("ne pişirsem" in soru or "ne yapsam" in soru or "ne yesem" in soru):
        return ["rastgele"]

    # Kategori eşleşmeleri
    kategori_eslestir = {
        "tatlı": "TATLI TARİFLERİ",
        "kurabiye": "KURABİYE TARİFLERİ",
        "köfte": "KÖFTE TARİFLERİ",
        "hamur": "HAMUR İŞİ TARİFLERİ",
        "kahvaltı": "KAHVALTILIK TARİFLERİ",
        "çorba": "ÇORBA TARİFLERİ",
        "salata": "SALATA TARİFLERİ",
    }

    
    for anahtar, kategori in kategori_eslestir.items():
        if anahtar in soru:
            return tarif_bul_kategori(kategori)

    """kelimeler = re.findall(r"\b\w+\b", soru)
    malzemeler = [k for k in kelimeler if k not in stopwords_tr]

    print("💬 Kullanıcının sorusu:", soru)
    print("🍅 Ayıklanan malzemeler:", malzemeler)"""

    # 🎯 3. Malzemeleri çıkar
    kelimeler = re.findall(r"\b\w+\b", soru)
    malzemeler = [
        k for k in kelimeler
        if k not in stopwords_tr and k not in fiil_filtresi
    ]

    print("💬 Kullanıcının sorusu:", soru)
    print("🍅 Ayıklanan malzemeler:", malzemeler)

    if malzemeler:
        return tarif_bul(malzemeler)

    return ["Anlayamadım 🫠"]