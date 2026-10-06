import json
import pprint
import zipfile
from collections import Counter
from pathlib import Path

import webcolors


def cp_categories_expand(zip_path, folder):
    """function to know total unique categories"""
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        arr = []
        total = 0
        for file in myzip.namelist():
            if folder in file and file.endswith(".json"):
                with myzip.open(file) as f:
                    data = json.load(f)
                    if type(data["count_objects"]) is dict:
                        continue
                    arr.append({"id": data["id"], "name": data["name"].capitalize(), "count": int(data.get("count_objects", 0))})
                    total += 1
    print(f'Total unique {folder} categories: {total}')
    return arr

def has_attributes(zip_path, folder, type_dict):
    """find objects with images, color within the top 12 categories (more than 2000 objects)"""
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        arr = []
        total = 0
        for file in myzip.namelist():
            if folder in file and file.endswith(".json"):
                with myzip.open(file) as f:
                    data = json.load(f)
                    try:
                        #print(data.get("type_id"))
                        #print(data.get("type_id") in type_dict)
                        if not data.get("type_id") in type_dict or not data.get("images") or not data.get("colors"):
                            #print("skipped")
                            continue
                        woa = {"title": data["title"], 
                               "type_id": data["type_id"],
                               "image": data["images"][0]["sq"]["url"],
                               "colors": data["colors"]
                            }
                        arr.append(woa)
                        total += 1
                    except Exception:  # noqa: S110
                        pass
    print(f'Total objects with images and colors in {folder} category: {total}')
    return arr

def get_closest_color_name(hex_code: str, spec: str = webcolors.CSS3) -> str:
    """
    Returns the exact or closest color name for a hex code using modern webcolors API.
    `spec` defaults to webcolors.CSS3 ('css3').
    """
    normalized_hex = webcolors.normalize_hex(hex_code) #fF0e9E -> ff0e9e
    try:
        return webcolors.hex_to_name(normalized_hex, spec=spec) #If hex is not exact, error raises
    except ValueError:
        pass

    target_rgb = webcolors.hex_to_rgb(normalized_hex) #convert hex to rgb
    closest_name = None
    min_distance = float('inf')

    """
    Iterates through all colors in CSS3 and measure distance against rgb
    Measure and store smallest distance and returns CSS3 name
    Need to further investigate the Euclidean distance thing.
    """
    for color_name in webcolors.names(spec=spec):
        color_rgb = webcolors.name_to_rgb(color_name, spec=spec)
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(target_rgb, color_rgb))
        
        if distance < min_distance:
            min_distance = distance
            closest_name = color_name

    return closest_name

home = Path.home() #Gives ypu the path to the home directory
zip_file_path = home / "Downloads" / "collection-master.zip" # / makes the path from home to downloads to the zip  
tot_types = 0      
                
cp_types = cp_categories_expand(zip_file_path, "types")
types_sort_by_count= sorted(cp_types, key = lambda x: x["count"],reverse=True)
types_2000 = [t for t in types_sort_by_count if t["count"] >= 2000] #array of top 12 categories

id_dict = {} #keyvalue pair of id and category name 

for woa in types_2000:
    woa_id = woa.get("id") #id is the category id
    woa_type_name = woa.get("name")
    id_dict[woa_id] = woa_type_name 

pprint.pp(id_dict)
woa_id_color = has_attributes(zip_file_path, "objects", id_dict) #returns  objects with colors and image within the specified categories

woa_groups = {}
#groups objects by category and color 
for woa in woa_id_color: #uses id to have the name of the category (groups by category)
    key = id_dict[woa["type_id"]]
    if key not in woa_groups:
        woa_groups[key] = {}
    try:
        i = 0
        primary_color = woa["colors"][i]["color"]
        color_name = get_closest_color_name(primary_color)
        while "gray" in color_name and len(woa["colors"]) > i + 1: #if the first color is gray, try the next one if not the objetc it gray
            i += 1
            primary_color = woa["colors"][i]["color"]
            color_name = get_closest_color_name(primary_color)
        if color_name not in woa_groups[key]: #groups by color
            woa_groups[key][color_name] = []
        woa_groups[key][color_name].append(woa)
    except (KeyError, IndexError):
        continue

d3_stack = []

for ctg in woa_groups: 
    category = ctg.capitalize()
    item = {"category": category}
    for color, value in woa_groups[ctg].items():
        item[color] = len(value)
    d3_stack.append(item)
    
""" with open(home / "Documents" / "00. DATA VIZ" / "02. MAJOR STUDIO" / "cooper_hewitt_viz" / "cooper_hewitt_by_category.json", "w") as f:
    json.dump(d3_stack, f, indent=4)
"""


"""


 obj_with_color = has_attributes(zip_file_path, "objects")

colors = {}

for obj in obj_with_color:
    try:
        i = 0
        primary_color = obj["colors"][i]["color"]
        color_name = get_closest_color_name(primary_color)
        while "gray" in color_name and len(obj["colors"]) > i + 1:
            i += 1
            primary_color = obj["colors"][i]["color"]
            color_name = get_closest_color_name(primary_color)
        if color_name not in colors:
            colors[color_name] = []
        colors[color_name].append(obj)
    except (KeyError, IndexError):
        continue

d3_treemap = {"name": "Cooper Hewitt Colors",
              "children": []}

for key, value in colors.items():
    color_name = key
    color_count = len(value)
    data_point = {"name": color_name, "value": color_count}
    d3_treemap["children"].append(data_point)

with open(home / "Documents" / "00. DATA VIZ" / "02. MAJOR STUDIO" / "cooper_hewitt_viz" / "cooper_hewitt_colors.json", "w") as f:
    json.dump(d3_treemap, f, indent=4)
 """
# working with Print Objects id 35236873 43099 objects / Textile 35251739 / Poster 35238163 
# Greeting Card 35285127 / Shopping Bag 35294605


