import json
import re
import random

# JSON verisini yükle
with open("cleaned_recipes_fixed.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

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
"""
# 🎯 Kategori bazlı eşleşme
def tarif_bul_kategori(kategori_adi):
    matches = [
        (r["Name"], 1, r["RecipeDetails"])
        for r in recipes
        if "CategoryBread" in r and r["CategoryBread"].upper() == kategori_adi.upper()
    ]
    if len(matches) > 3:
        return random.sample(matches, 3)
    elif matches:
        return matches
    else:
        return ["Bu kategoriye ait tarif bulunamadı 🤔"]

# 🎯 Malzeme bazlı eşleşme (esnek & ALL mantığı)
def tarif_bul(malzemeler):
    matches = []
    for r in recipes:
        # Tarif malzemelerini parçala (örneğin: 'dana kıyma', 'patates', 'sarımsak')
        tarif_kelimeleri = [w.lower().strip() for i in r["IngridientNames"].split(";") for w in i.split()]
        
        # Her malzemenin tarifte geçip geçmediğini kontrol et (esnek eşleşme)
        tumu_var_mi = all(
            any(m in tk or tk in m for tk in tarif_kelimeleri)
            for m in malzemeler
        )

        if tumu_var_mi:
            matches.append((r["Name"], len(malzemeler), r["RecipeDetails"]))

    # ❌ Hiçbir tarif bulunamadıysa
    if not matches:
        return ["Sorunu tam anlayamadım 🤔 Daha açık yazar mısın ya da farklı bir şekilde sorar mısın?"]

    # ✅ Eğer sadece 1 malzeme verdiyse → sadece 1 tane rastgele tarif
    if len(malzemeler) == 1:
        return [random.choice(matches)]

    # ✅ Diğer durumlarda max 3 tarif döndür
    if len(matches) > 3:
        return random.sample(matches, 3)

    return matches
"""

def tarif_bul_kategori(kategori_adi):
    matches = [
        {
            "isim": r["Name"],
            "malzemeler": r["IngridientNames"],
            "tarif": r["RecipeDetails"].split("\n")
        }
        for r in recipes
        if "CategoryBread" in r and r["CategoryBread"].upper() == kategori_adi.upper()
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
        tarif_kelimeleri = [w.lower().strip() for i in r["IngridientNames"].split(";") for w in i.split()]
        
        tumu_var_mi = all(
            any(m in tk or tk in m for tk in tarif_kelimeleri)
            for m in malzemeler
        )

        if tumu_var_mi:
            matches.append({
                "isim": r["Name"],
                "malzemeler": r["IngridientNames"],
                "tarif": r["RecipeDetails"].split("\n")
            })

    if not matches:
        return ["Sorunu tam anlayamadım  Daha açık yazar mısın ya da farklı bir şekilde sorar mısın?"]

    if len(malzemeler) == 1:
        return [random.choice(matches)]

    if len(matches) > 3:
        return random.sample(matches, 1)

    return matches