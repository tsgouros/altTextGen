
import os
import openai
import pandas as pd
import ast
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
from k_means import classify_text
from gpt import evaluate_description

openai.api_key = "lalalala"
categories = {
    "Colors and Descriptions": {"blue", "light", "bright", "white", "black", "red", "orange", "yellow", "pink", "green", "color", "colorful", "shades"},
    "Spatial Directions and Positions": {"left", "right", "top", "bottom", "center", "below", "above", "up", "down", "side"},
    "Astronomical Terms": {"galaxies", "galaxy", "star", "stars", "telescope", "planet", "nebula", "rings", "dust", "gas", "core", "disk", "cluster", "sphere", "arms", "area", "field", "outer", "distant", "region", "central", "material", "thin"},
    "Visualization Elements": {"image", "graphic", "illustration", "infographic", "arrows", "key", "dots", "mirror", "lines", "shapes", "panel", "sizes", "oval", "wispy"},
    "Telescope and Instrument Names": {"nasa", "chandra", "X-Ray" "webb", "nircam", "microns", "nirspec", "miri"},
    "Text and Labels": {"labeled", "titled", "showing", "shows", "points", "appear", "throughout", "representing"},
    "Measurement and Data": {"scale", "wavelength", "diffraction", "spectrum", "brightness"},
    "Direction and Movement": {"there", "out", "around", "toward", "horizontal", "vertical", "across", "between", "create", "sizes"},
    "Quantitative Terms": {"three", "more", "few", "many", "most", "some", "about", "time", "while"},
    "Other Terms": {"arrows", "key", "clock", "indicate", "field", "cloud", "clouds", "also", "hubble", "exoplanet", "used", "miri", "oval"}
}

high_quality_means = np.array([0.952344, 0.924219, 0.954688, 0.882812, 0.369531, 0.864844, 0.582812, 0.868750, 0.842969, 0.797656, 0.878125, 0.964063, 0.933594, 0.978125])
low_quality_means = np.array([0.159259, 0.062963, 0.338889, 0.072222, 0.092593, 0.066667, 0.011111, 0.037037, 0.012963, 0.051852, 0.540741, 0.275926, 0.466667, 0.312963])
moderate_quality_means = np.array([0.505405, 0.064865, 0.540541, 0.054054, 0.000000, 0.067568, 0.000000, 0.008108, 0.008108, 0.029730, 0.905405, 0.621622, 0.791892, 0.772973])
ranges = np.max([high_quality_means, moderate_quality_means, low_quality_means], axis=0) - np.min([high_quality_means, moderate_quality_means, low_quality_means], axis=0)

def evaluate_multiple(directory):
    # pair_path = os.path.join(directory, pair_folder)

    # urls = os.path.join(directory, 'image_descriptions_urls.txt')
    # with open(urls, 'r') as file:
    #     lines = [line.strip().strip("(),'") for line in file if line.strip()]
    #     image_urls = lines

    pair_directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and 'pair_' in d]


    descriptions = []
    classifications = []
        
    for i, pair_dir in enumerate(pair_directories):
        if i >= 1:  # Stop after processing 10 images
                break

        pair_folder = f"pair_{i}"
        pair_path = os.path.join(directory, pair_folder)

        with open(os.path.join(pair_path, 'description.txt'), 'r') as good_file:
            good_text = good_file.read()

        with open(os.path.join(pair_path, 'b_description.txt'), 'r') as bad_file:
            bad_text = bad_file.read()

        url_path = os.path.join(pair_path, 'url.txt')

        with open(url_path, 'r') as file:
            image_url = file.read().strip("(),'")

        good_scores_vector = evaluate_description(good_text, image_url)
        bad_scores_vector = evaluate_description(bad_text, image_url)

        good_classification = classify_text(good_scores_vector)
        bad_classification = classify_text(bad_scores_vector)

        descriptions.append((good_text, good_scores_vector))
        descriptions.append((bad_text, bad_scores_vector))
       

        classifications.append((good_scores_vector,good_classification))
        classifications.append((bad_scores_vector, bad_classification))

    print(classifications)

evaluate_multiple('facts_pairs')

     
def evaluate_single(description, img_url):
    score_vector= evaluate_description(description, img_url)
    classification = classify_text(score_vector)

    print(classification)


evaluate_single('A red and blue planet in space','https://chandra.harvard.edu/photo/2023/sn1006/sn1006.jpg' )
        



