import pickle # loading serialized data from a file.
#from colorthief import ColorThief
from webcolors import rgb_to_name
from PIL import Image
import io #handling byte streams
import json
import matplotlib.pyplot as plt

# Import the Packages
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.image as mpimg

from scipy.spatial import KDTree #searches of nearest neighbors in space (used for matching colors).
from webcolors import (
    CSS3_HEX_TO_NAMES,
    CSS21_HEX_TO_NAMES,
    hex_to_rgb,
)

# after kmeans use euclidean dist to get other usable colors
#RGB color tuple as input and returns the closest CSS3 color name
# by using a KD-Tree for fast nearest neighbor search among predefined CSS3 colors.
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

#Uses KMeans clustering to find n_colors dominant colors.
# Converts the RGB values of cluster centers to color names.
# Returns a list of unique color names.

#ENDOGENOUS FACT CHECKING
def get_colors_from_image(image_bytes, n_colors=30):
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    depth = 3  # Assuming RGB image
    # Reshape the image into a 2D array
    pixel = np.array(image).reshape((width * height, depth))
    
    # Set the desired number of colors for the image
    #n_colors = 10
    n_colors = 10
    
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
    img_type = metadata[0].lower()
    obj_type = metadata[1].lower()
    obj_name = metadata[2].lower()

    color_names = [name for hex_code, name in CSS21_HEX_TO_NAMES.items()]
    alt_text_score = 0
    lower_alt_text = str(alt_text).lower()
    words = lower_alt_text.split()
    print("alt text:", alt_text)

    # check for image type
    if img_type not in lower_alt_text:
        alt_text_score = -1
        print("img type not in alt text", img_type)
    else:
        print("img type is in alt!", img_type)
    if obj_type not in lower_alt_text:
        alt_text_score = -1
        print("obj type not in alt text", obj_type)
    else:
        print("obj type is in alt!", obj_type)
    if obj_name not in lower_alt_text:
        alt_text_score = -1
        print("obj name not in alt text", obj_name)
    else:
        print("obj name is in alt!", obj_name)

    for word in words:
        # if word is a color we know (could have been extracted from image), make sure it was extracted from the image
        if word in color_names and word not in colors:
            alt_text_score = -1
            print("found this color in alt text that wasn't in the image", word)   
        elif word in color_names and word in colors:
            # raise score to 0 if it at least found 1 overlapping color
            print("found color", word)  
    print("\n")    
    return alt_text_score

def create_master_lists(data):
    master_img_types = set()
    master_obj_types = set()
    master_obj_names = set()

    for entry in data.values():
        metadata = entry['info']  # Assuming 'info' is a list like [img_type, obj_type, obj_name]
        master_img_types.add(metadata[0].lower())
        master_obj_types.add(metadata[1].lower())
        master_obj_names.add(metadata[2].lower())

    return master_img_types, master_obj_types, master_obj_names

def load_data_from_pickle(pickle_file_path):
    with open(pickle_file_path, 'rb') as handle:
        data = pickle.load(handle)
    return data
    
pickle_file_path = "all_pdf_info_r3.pkl"
data = load_data_from_pickle(pickle_file_path)

master_img_types, master_obj_types, master_obj_names = create_master_lists(data)

def process_alt_text_binary(alt_text, metadata, colors):
    global master_img_types, master_obj_types, master_obj_names 

    img_type = metadata[0].lower()
    obj_type = metadata[1].lower()
    obj_name = metadata[2].lower()

    color_names = [name for hex_code, name in CSS21_HEX_TO_NAMES.items()]
    pass_check = True
    failure_reasons = []
    
    lower_alt_text = str(alt_text).lower()
    words = lower_alt_text.split()
    print("alt text:", alt_text)

    # check for image type

    #EXOGENOUS
    if img_type not in lower_alt_text:
        pass_check = False
        failure_reasons.append(f"Image type '{img_type}' not in alt text.")
        

    if obj_type not in lower_alt_text:
        pass_check = False
        failure_reasons.append(f"Object type '{obj_type}' not in alt text.")
        

    if obj_name not in lower_alt_text:
        pass_check = False
        failure_reasons.append(f"Object Name '{obj_name}' not in alt text.")

    #FALSE POSITIVES CHECK
    for word in words:
        # Check if any word matches a master list entry but not the current metadata
        if word in master_img_types and img_type != word:
            pass_check = False
            failure_reasons.append(f"False image type mentioned: {word}")
        if word in master_obj_types and obj_type != word:
            pass_check = False
            failure_reasons.append(f"False object type mentioned: {word}")
        if word in master_obj_names and obj_name != word:
            pass_check = False
            failure_reasons.append(f"False object name mentioned: {word}")    
        
    #ENDOGENOUS
        
    #changed this,  more efficient by creating a set of words from the alt text and
    #then finding the intersection with the set of known color names so that each color is only checked once, 
    words = set(lower_alt_text.split())
    mentioned_colors = words.intersection(set(color_names)) #colors in alt text
    extracted_colors_set = set(colors) #colors from imsge

    if not mentioned_colors.intersection(extracted_colors_set):
        pass_check = False
        failure_reasons.append("None of the extracted colors are mentioned in the alt text.")

    unmatched_colors = mentioned_colors.difference(extracted_colors_set) #to find any colors mentioned in the alt text 
    #that do not appear in the set of colors extracted from the image.
    
    if unmatched_colors:
        pass_check = False
        unmatched_color_str = ", ".join(unmatched_colors)
        failure_reasons.append(f"Mentioned colors not in image: {unmatched_color_str}.")
    
    if pass_check:
        return "Pass", []
    else:
        return "Fail", failure_reasons

def process_files(pickle_file_path, alt_text_file_path):
    with open(pickle_file_path, 'rb') as handle:
        data = pickle.load(handle)
    with open(alt_text_file_path, 'r') as file:
        alt_texts = json.load(file)
    entryToAltDict = {}
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

        # check for first good score (all colors in alt are in img, all metadata is in alt)
        if 0 in alt_text_scores:
            goodaltInd = alt_text_scores.index(0)
            goodalt = alt_texts[entry][goodaltInd]
            entryToAltDict[entry] = goodalt
            print("first good alt text:", goodalt)
        else:
            entryToAltDict[entry] = ""

    # save dict from img number key to the good alt text
    with open('entryToCheckedAltText.json', 'w') as json_file:
        json.dump(entryToAltDict, json_file)

def process_files_binary(pickle_file_path, alt_text_file_path):
    with open(pickle_file_path, 'rb') as handle:
        data = pickle.load(handle)
    with open(alt_text_file_path, 'r') as file:
        alt_texts = json.load(file)

    #for binary
    entryToAltDict = {}
    entryToFailReasonsDict = {}
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
        alt_text_evaluations = []
        #modified to handle 
        for alt_text in alt_texts[entry]:
            result, reasons = process_alt_text(alt_text, metadata, colors)
            alt_text_evaluations.append((alt_text, result, reasons))
        
        # Find the first passing alt text or store failure reasons
        pass_found = False
        for alt_text, result, reasons in alt_text_evaluations:
            if result == "Pass":
                entryToAltDict[entry] = alt_text
                print(f"Passing alt text found: {alt_text}")
                pass_found = True
                break
            else:
                entryToFailReasonsDict[entry] = reasons
        
        if not pass_found:
            print(f"No passing alt text found for entry {entry}. See failure reasons.")
            entryToAltDict[entry] = ""  # Indicate no passing alt text found
    

    # Save the mapping of entries to their evaluated alt texts
    with open('entryToCheckedAltText.json', 'w') as json_file:
        json.dump(entryToAltDict, json_file)
    
    # Optionally, save the failure reasons for entries without a passing alt text
    with open('entryToFailReasons.json', 'w') as json_file:
        json.dump(entryToFailReasonsDict, json_file)

if __name__ == "__main__":
    pickle_file_path = "all_pdf_info_r3.pkl"
    alt_text_file_path = "generated_alttext_all.json"
   
    process_files(pickle_file_path, alt_text_file_path)
