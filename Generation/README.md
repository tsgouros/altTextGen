# Alt-text Generation with InstructBLIP
This jupyter notbook contains a demostration of how to use InstructBLIP to generate alt-texts for astronomical images. 

Requirements: \
torch==2.1.1 \
openai==1.3.5 \
transformers==4.34.0 \






## Note on the generated alt-text json file
The `generated_alttext_all.json` file contains the generated alt texts of 645 image releases by the Chandra X-ray Observatory. The json file is structured so that each image entry is represented by a string YEAR_NAME, where YEAR is the last two digits of the year the image is published on the Chandra website, and NAME is the name of the image entry. For example, `00_0015` points to an image entry from 2000, and the name of the image is 0015. You can construct a URL link from this information to see the web page - https://chandra.cfa.harvard.edu/photo/2000/0015/. 
