# altTextGen
Generating alt-text image descriptions with a large language model.

Please establish these directories: 

  evaluation
  generation
  factChecking
  utils

Then go populate them!

Running the Evaluation:
-  This pipeline evaluates alttext descriptions of images using a two-step process involving AI-generated scores (using gpt.py) and cluster analysis (k_means.py). 

To run it you need:
-  Python 3.x
-  Libraries: pandas, sklearn, matplotlib, numpy, openai, install using: pip install pandas sklearn matplotlib numpy openai
-  An OpenAI API key for GPT-4 access



File Structure
Scripts:

-  gpt.py: Generates evaluation scores for image descriptions.
-  k_means.py: Performs clustering on these scores to categorize the quality of descriptions.
-  
Directories and Files:
-  url_pairs/image_description_urls.txt: Contains URLs of images.
-  full_pairs/: Contains pair_X subdirectories with description.txt (good alt texts) and b_description.txt (bad alt texts) for each image.
-  evaluation_scores_full4.txt: Output from gpt.py in the form of vector scores for the image, input for k_means.py.
-  the evaluation_scores_full4.txt is used to tran our classification model.
-  for new alt texts, generate score vectors using gpt.py. then, pass these vectors into the classify_text() function in k_means.py to obtain a quality label for the texts.
