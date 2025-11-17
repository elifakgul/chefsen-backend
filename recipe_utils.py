import json
import os
import random
from django.conf import settings  # 🔥 BASE_DIR için

# JSON dosyasının tam yolu (repo kökünde duruyor)
JSON_PATH = os.path.join(settings.BASE_DIR, "cleaned_recipes_fixed.json")

# JSON verisini yükle
try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
except FileNotFoundError:
    print(f"[recipe_utils] JSON bulunamadı: {JSON_PATH}")
    raw_data = {}

# Tarifleri al
all_recipes = raw_data.get("Recipe", {})

# Geçerli tarifleri filtrele
recipes = [
    r for r in all_recipes.values()
    if isinstance(r, dict)
    and "Name" in r
    and "IngridientNames" in r
    and isinstance(r["IngridientNames"], str)
]


def tarif_bul_kategori(kategori_adi):
    matches = [
        {
            "isim": r["Name"],
            "malzemeler": r.get("IngridientNames", ""),
            "tarif": r.get("RecipeDetails", "").split("\n"),
        }
        for r in recipes
        if "CategoryBread" in r
        and isinstance(r["CategoryBread"], str)
        and r["CategoryBread"].upper() == kategori_adi.upper()
    ]

    if len(matches) > 3:
        return random.sample(matches, 3)
    elif matches:
        return matches
    else:
        return ["Bu kategoriye ait tarif bulunamadı "]


def tarif_bul(malzemeler):
    matches = []
    for r in recipes:
        ing = r.get("IngridientNames")
        if not isinstance(ing, str):
            continue

        # Malzemeleri parçala
        tarif_kelimeleri = [
            w.lower().strip()
            for i in ing.split(";")
            for w in i.split()
        ]

        # Her malzeme tarifte esnek olarak geçiyor mu?
        tumu_var_mi = all(
            any(m in tk or tk in m for tk in tarif_kelimeleri)
            for m in malzemeler
        )

        if tumu_var_mi:
            matches.append({
                "isim": r["Name"],
                "malzemeler": ing,
                "tarif": r.get("RecipeDetails", "").split("\n"),
            })

    if not matches:
        return ["Sorunu tam anlayamadım  Daha açık yazar mısın ya da farklı bir şekilde sorar mısın?"]

    if len(malzemeler) == 1:
        return [random.choice(matches)]

    if len(matches) > 3:
        # Önce 1 tane dönüyordun, istersen 3 yapabilirsin
        return random.sample(matches, 1)

    return matches
