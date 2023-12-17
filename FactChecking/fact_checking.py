import pickle
from colorthief import ColorThief
from webcolors import rgb_to_name
from PIL import Image
import io
import json
import matplotlib.pyplot as plt

# Import the Packages
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.image as mpimg

from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    CSS21_HEX_TO_NAMES,
    hex_to_rgb,
)

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS21_HEX_TO_NAMES
    names = []
    rgb_values = []    
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)    
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'

def get_colors_from_image(image_bytes, n_colors=30):
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    depth = 3  # Assuming RGB image
    # Reshape the image into a 2D array
    pixel = np.array(image).reshape((width * height, depth))
    
    # Set the desired number of colors for the image
    # n_colors = 10
    
    # Create a KMeans model with the specified number of clusters and fit it to the pixels
    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixel)
    
    # Get the cluster centers (representing colors) from the model
    colour_palette = np.uint8(model.cluster_centers_)

    # Process image colors
    result = [convert_rgb_to_names(tuple(color)) for color in colour_palette]
    return list(set(result))

# function to process 1 alt text given the alt text string, extracted colors and image metadata
# color extraction isn't done in this function since it only has to happen once per image, not per alt text
def process_alt_text(alt_text, metadata, colors):
    # img_type = metadata[0].lower().split()
    # obj_type = metadata[1].lower().split()
    # ob_name = metadata[2].lower().split()
    # has_img_type = False
    # isAccurate = True
    # metadata not used for processing yet bc each piece has multiple words/punct and we want to check not only that they are there but also that there is no incorrect data
    color_names = [name for hex_code, name in CSS21_HEX_TO_NAMES.items()]
    alt_text_score = -1
    words = str(alt_text).split()
    print("alt text:", alt_text)
    for word in words:
        # if word is a color we know (could have been extracted from image), make sure it was extracted from the image
        if word in color_names and word not in colors:
            alt_text_score = -1
            print("found this color in alt text that wasn't in the image", word)   
        elif word in color_names and word in colors:
            # raise score to 0 if it at least found 1 overlapping color
            alt_text_score = 0
            print("found color", word)  
    print("\n")    
    return alt_text_score

def process_files(pickle_file_path, alt_text_file_path):
    with open(pickle_file_path, 'rb') as handle:
        data = pickle.load(handle)
    with open(alt_text_file_path, 'r') as file:
        alt_texts = json.load(file)

    for entry in data:
        print("entry: " + str(entry))
        
        #print(str(data[entry].keys()))
        captions = data[entry]['text']
        #print(str(captions))
        metadata = data[entry]['info']
        #print("metadata: " + str(metadata))
        image_bytes = data[entry]['image']

        # get image colors
        colors = get_colors_from_image(image_bytes)

        #Print or store the results as needed
        print("Captions:", captions)
        print("Metadata:", metadata)
        print("result colors:", colors)

        #check each alt text for colors and metadata
        alt_text_scores = []
        for i in range(20):
            score = process_alt_text(alt_texts[entry][i], metadata, colors)
            alt_text_scores.append(score)
        print("scores: " + str(alt_text_scores))

if __name__ == "__main__":
    pickle_file_path = "all_pdf_info_r3.pkl"
    alt_text_file_path = "generated_alttext_all.json"
   
    process_files(pickle_file_path, alt_text_file_path)
