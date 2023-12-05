
import os
import base64
import openai

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



openai.api_key = "lalalalala"


import ast

#using urls insteadof encoding to base64 str
with open('url_pairs/image_description_urls.txt', 'r') as file:
    lines = [line.strip().strip("(),'") for line in file if line.strip()]
    image_urls = lines

#based on response structure
def parse_scores_to_vector(response_text):
    lines = [line.strip() for line in response_text.strip().split('\n') if line]
    scores_vector = []

    for line in lines:
        if 'Vector'in line:
            # get the list from the string
            vector_str = line.split(':', 1)[1].strip()
            try:
                #string representation of a list to a literal list
                scores_vector = ast.literal_eval(vector_str)
            except (ValueError, SyntaxError) as e:
                print(f"Could not parse the vector: {vector_str}")
                scores_vector = None
        else:
            parts = line.split(':')
            if len(parts) == 2:
                _, score_str = parts
                score_cleaned = score_str.strip()
                try:
                    score = float(score_cleaned)
                    scores_vector.append(score)
                except ValueError as e:
                    #might be due to the 'Vector:' line or something.
                    continue
    
    return scores_vector



def evaluate_description(text, image_url):
    
    prompt = [
        
        {
            "role": "user",
            "content": [
                 {"type": "text", "text": "First, read this alt text description, then the corresponding image"},
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": "Please evaluate the following alt-text description in relation to the accompanying image, focusing on two aspects for the first ten dimensions: the usage of specific key terms and the adherence to the criteria detailed in each dimension. For the remaining four dimensions, evaluate based on the descriptions provided. Provide a floating point score between 0 (poor) and 1 (excellent) for each dimension. Do not give scores of N/A. A score must be given to each dimension, if a score is not applicable, give a score of 0.  Combine all 14 scores in a vector to represent the total rating of the text. Evaluation criteria and key terms for each dimension: - Colors and Descriptions: Evaluate based on how well the text uses terms such as blue, light, bright, white, black, red, orange, yellow, pink, green, color, colorful, shades. - Spatial Directions and Positions: Evaluate using terms like left, right, top, bottom, center, below, above, up, down, side. - Astronomical Terms: Assess usage of galaxies, galaxy, star, stars, telescope, planet, nebula, rings, dust, gas, core, disk, cluster, sphere, arms, area, field, outer, distant, region, central, material, thin. - Visualization Elements: Check for image, graphic, illustration, infographic, arrows, key, dots, mirror, lines, shapes, panel, sizes, oval, wispy. - Telescope and Instrument Names: Includes chandra, NASA, webb, nircam, microns, nirspec, miri. - Text and Labels: Look for labeled, titled, showing, shows, points, appear, throughout, representing. - Measurement and Data: Focus on scale, wavelength, diffraction, spectrum, brightness. - Direction and Movement: Terms like there, out, around, toward, horizontal, vertical, across, between, create, sizes. - Quantitative Terms: Use of three, more, few, many, most, some, about, time, while. - Other Terms: Includes arrows, key, clock, indicate, field, cloud, clouds, also, hubble, exoplanet, used, miri, oval. - Conciseness: Is the text concise yet informative? - Accuracy: How accurate is the description in representing the image? - Clarity: Is the description clear and easy to understand? - Relevance: Are all parts of the description relevant to the image? Provide a short justification for the scores based on the given evaluation criteria. Present the scores in a vector format as Vector: [], corresponding to the order of the dimensions listed above."},
            ]
        },
        
    ]

    
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=prompt,
        max_tokens=1000
    )

    last_message = response['choices'][0]['message']['content'] if response['choices'] else None
    print(response['choices'][0]['message']['content'])

    if last_message: #element by element
        scores_vector = parse_scores_to_vector(last_message)
    else:
        scores_vector = None

    return scores_vector


directory = "full_pairs"
output_file = "evaluation_scores_full5.txt"



with open(output_file, 'w') as file:
    for i, image_url in enumerate(image_urls):
        # if i >= 3:  # Stop after processing 10 images
        #     break
        pair_folder = f"pair_{i}"
        pair_path = os.path.join(directory, pair_folder)

        with open(os.path.join(pair_path, 'description.txt'), 'r') as good_file:
            good_text = good_file.read()

        with open(os.path.join(pair_path, 'b_description.txt'), 'r') as bad_file:
            bad_text = bad_file.read()

        good_scores_vector = evaluate_description(good_text, image_url)
        bad_scores_vector = evaluate_description(bad_text, image_url)

        # print(good_text)
        # print(bad_text)

        
        file.write(f"Scores for {pair_folder} - Good Text: {good_scores_vector}\n")
        file.write(f"Scores for {pair_folder} - Bad Text: {bad_scores_vector}\n")
        file.write('\n')  

print(f"Scores have been written to {output_file}")

#include fact check
#update dim 4
#
