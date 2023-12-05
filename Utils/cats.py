import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
import re

nltk.download('punkt')

def analyze_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in excluded_terms]
    freq_dist = FreqDist(tokens)
    return freq_dist

# define excluded terms and punctuation
excluded_terms = {
    "the", ",", ".", "a", "of", "and", "is", "with", "to", "in", "are", "at", "from", "on", "that", "its", ":"
}

# define categories
categories = {
    "Colors and Descriptions": {"blue", "light", "bright", "white", "black", "red", "orange", "yellow", "pink", "green", "color", "colorful", "shades"},
    "Spatial Directions and Positions": {"left", "right", "top", "bottom", "center", "below", "above", "up", "down", "side"},
    "Astronomical Terms": {"galaxies", "galaxy", "star", "stars", "telescope", "planet", "nebula", "rings", "dust", "gas", "core", "disk", "cluster", "sphere", "arms", "area", "field", "outer", "distant", "region", "central", "material", "thin"},
    "Visualization Elements": {"image", "graphic", "illustration", "infographic", "arrows", "key", "dots", "mirror", "lines", "shapes", "panel", "sizes", "oval", "wispy"},
    "Telescope and Instrument Names": {"webb", "nircam", "microns", "nirspec", "miri"},
    "Text and Labels": {"labeled", "titled", "showing", "shows", "points", "appear", "throughout", "representing"},
    "Measurement and Data": {"scale", "wavelength", "diffraction", "spectrum", "brightness"},
    "Direction and Movement": {"there", "out", "around", "toward", "horizontal", "vertical", "across", "between", "create", "sizes"},
    "Quantitative Terms": {"three", "more", "few", "many", "most", "some", "about", "time", "while"},
    "Other Terms": {"arrows", "key", "clock", "indicate", "field", "cloud", "clouds", "also", "hubble", "exoplanet", "used", "miri", "oval"}
}

csv_file = 'alt_data.csv'
output_file = 'common_categories.txt'
df = pd.read_csv(csv_file)

# dictionary to store category frequencies
category_freq = {category: 0 for category in categories}

for alt_text in df['Alt Text']:
    freq_dist = analyze_text(alt_text)
    for category, category_words in categories.items():
        category_freq[category] += sum(freq_dist[word] for word in category_words)

# sort the categories by frequency
sorted_categories = sorted(category_freq.items(), key=lambda x: x[1], reverse=True)

# save the most common categories to a text file
with open(output_file, 'w') as file:
    file.write("Category\tFrequency\n")
    for category, frequency in sorted_categories:
        file.write(f"{category}\t{frequency}\n")

print(f"Common categories and their frequencies saved to {output_file}")
