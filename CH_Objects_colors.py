

import zipfile
import json
from pathlib import Path
from collections import Counter
import webcolors

home = Path.home()
zip_file_path = home / "Downloads" / "collection-master.zip"

def get_closest_color_name(hex_code: str, spec: str = webcolors.CSS3) -> str:
    """Retorna el nombre CSS3 más cercano para un código hexadecimal."""
    normalized_hex = webcolors.normalize_hex(hex_code)
    try:
        return webcolors.hex_to_name(normalized_hex, spec=spec)
    except ValueError:
        pass

    target_rgb = webcolors.hex_to_rgb(normalized_hex)
    closest_name = None
    min_distance = float('inf')

    for color_name in webcolors.names(spec=spec):
        color_rgb = webcolors.name_to_rgb(color_name, spec=spec)
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(target_rgb, color_rgb))
        
        if distance < min_distance:
            min_distance = distance
            closest_name = color_name

    return closest_name

def cp_categories_expand(zip_path, folder):
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        types_arr = []
        total = 0
        for file in myzip.namelist():
            if folder in file and file.endswith(".json"):
                with myzip.open(file) as f:
                    data = json.load(f)
                    if type(data["count_objects"]) is dict:
                        continue
                    types_arr.append({"id": data["id"], "name": data["name"], "count": int(data.get("count_objects", 0))})
                    total += 1
    return types_arr

def get_woa_by_type(zip_path, type_id):
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        arr = []
        total = 0
        for file in myzip.namelist():
            if "/objects" in file and file.endswith(".json"):
                with myzip.open(file) as f:
                    data = json.load(f)
                    if data.get("type_id") == type_id:
                        if not data.get("images") or not data.get("colors") or not data.get("decade"):
                            continue
                        woa = {
                            "title": data["title"],
                            "decade": data["decade"],
                            "image": data["images"][0]["sq"]["url"],
                            "colors": data["colors"]
                        }
                        arr.append(woa)
                        total += 1
        print(f'Total Objects by category: {total}')
    return arr        

if __name__ == "__main__":
    cp_types = cp_categories_expand(zip_file_path, "types")
    types_sort_by_count = sorted(cp_types, key=lambda x: x["count"], reverse=True)

    # ID  Textils: 35251739
    arr = get_woa_by_type(zip_file_path, "35251739")

    decades = {}
    for woa in arr:
        decade = woa["decade"]
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(woa)

    color_vals = {}
    for decade, woas in decades.items(): 
        counts = Counter()
        for woa in woas:
            for color in woa["colors"]:
                hex_code = color["color"]
                CSS3_name = get_closest_color_name(hex_code)
                counts[CSS3_name] += 1
        color_vals[decade] = counts.most_common()

  
    with open("Textiles_Colors_By_Decade1.json", "w") as f: 
        json.dump(color_vals, f)