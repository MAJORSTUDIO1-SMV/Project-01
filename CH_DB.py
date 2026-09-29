import zipfile
import json
import pprint

from pathlib import Path
from collections import Counter

import webcolors # module for with utilities for web colors 

"""
    Path is a module, helps you navigate through directories and files. 
    One of the key benefits of using Path is os compability.
"""
home = Path.home() #Gives ypu the path to the home directory
zip_file_path = home / "Downloads" / "collection-master.zip" # / makes the path from home to downloads to the zip  

def get_closest_color_name(hex_code: str, spec: str = webcolors.CSS3) -> str: # function returns the closest color match name in css3
    """
    Returns the exact or closest color name for a hex code using modern webcolors API.
    `spec` defaults to webcolors.CSS3 ('css3').
    """
    normalized_hex = webcolors.normalize_hex(hex_code) #fF0e9E -> ff0e9e puts the hex value in the correct format
    try:
        return webcolors.hex_to_name(normalized_hex, spec=spec) #If hex is not exact, error 
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

# working with Print Objects id 35236873 / Textile 35251739 / Poster 35238163 
# Greeting Card 35285127 / Shopping Bag 35294605


#  the first part of the code searchs the zip for objects that has information for color, image and decade 


with zipfile.ZipFile(zip_file_path, 'r') as myzip: #give the function the path and what I want to do with it (read)
        """
        This code creates an an array for all objects with Textile type_id
        that have images, and color and decade data
        """
        arr = []
        total = 0
        for file in myzip.namelist(): #.namelist creates a list of all directories and files in a zip
            if "/objects" in file and file.endswith(".json"): #filter for paths that are in the objects folder and are .json files
                with myzip.open(file) as f:
                    data = json.load(f) #create a dict with json data of the object
                    if data.get("type_id") == "35251739": #match id or skip to next
                        if not data.get("images") or not data.get("colors") or not data.get("decade"):#look for and filter object that have img, colors and decade or skip
                            continue
                        woa = {"title": data["title"], # create a new subset of the information that i need 
                               "decade": data["decade"],
                               "image": data["images"][0]["sq"]["url"],
                               "colors": data["colors"]
                                }
                        arr.append(woa)
                        total += 1
        print(f'Total print works of art (WOA) with image in Textile category: {total}')





# categorize all woas into decade arrays 

decades = {} # dictonary to group woas by dacade


for woa in arr: # makes an array for every decade 
    decade = woa["decade"]
    if decade not in decades:
        decades[decade] = []
    decades[decade].append(woa) 
    




# counts how many times a color appears in each decade 

color_vals = {} #dictonary for the colors 


# Loop through all woas colors in each decade and get CSS3 name 
# Order colors by descending popularity


for decade, woas in decades.items(): 
    counts = Counter()
    for woa in woas:
        #print(woa)
        for color in woa["colors"]:
            hex_code = color["color"]
            CSS3_name = get_closest_color_name(hex_code)
            counts[CSS3_name] += 1
    color_vals[decade] = counts.most_common()

# Save color_vals dict as json to be able to use the set as my database

with open(home / "Downloads" / "Textiles_Colors_By_Decade.json","w") as f: 
    data_json = json.dump(color_vals, f)
