from bs4 import BeautifulSoup
import requests
import os

url = 'https://chandra.harvard.edu/photo/description_audio.html'  

response = requests.get(url)
response.raise_for_status()  #   exception if the request was unsuccessful

# parse the HTML content 
soup = BeautifulSoup(response.text, 'html.parser')

img_tags = soup.find_all('img')[2:]  # (decorative images)
description_links = soup.find_all('a', href=True)

images = []
descriptions = []

#these will hold the links

for img in img_tags:
    src = img.get('src')
    if src:
        #for relative URLs, add the base URL
        img_url = src if src.startswith(('http://', 'https://')) else 'https://chandra.harvard.edu' + src
        
        # Remove '_thm'  to get the high-res version
        high_res_img_url = img_url.replace('_thm', '')
        images.append(high_res_img_url)

for link in description_links:
    href = link.get('href')
    if href and "description.txt" in href:
        # If the link is a relative URL, add the base URL
        link_url = href if href.startswith(('http://', 'https://')) else 'https://chandra.harvard.edu' + href
        descriptions.append(link_url)



# output_directory = 'url_pairs'
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

# # File to write the URLs
# output_file = os.path.join(output_directory, 'image_description_urls.txt')

# # Writing URLs to the output file
# with open(output_file, 'w') as file:
#     for img_url in zip(images):
#         file.write(f"{img_url}\n")

# print(f"URLs have been written to {output_file}")
#directory to hold pairs
if not os.path.exists('pairs'):
    os.makedirs('pairs')

# downloading all
for i, (img_url, desc_url) in enumerate(zip(images, descriptions)):
    #  sub-dir for each pair
    pair_folder = f'pairs/pair_{i}'
    if not os.path.exists(pair_folder):
        os.makedirs(pair_folder)

    try:
        #  image
        img_data = requests.get(img_url).content
        with open(f'{pair_folder}/image.jpg', 'wb') as img_file:
            img_file.write(img_data)
        print(f'Image {i} downloaded: {img_url}')

        #  description
        desc_data = requests.get(desc_url).content
        with open(f'{pair_folder}/description.txt', 'wb') as desc_file:
            desc_file.write(desc_data)
        print(f'Description {i} downloaded: {desc_url}')
    except requests.RequestException as e:
        print(f'Error downloading {img_url} or {desc_url}: {e}')


# to-do:
# - download all webb img/alt pairs
# - ask etha to get ppt txts for webb
# - create one doc with img-good txt-bad txt (one just for chandra, one for chnadra+web)
# -set up API integration
# - work on tweaking prompts to got4 for more useful scoring
# - get vector scores for 'bad' and 'good' for each images
# - pca stuff!