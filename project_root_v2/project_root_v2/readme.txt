README.txt
==========

This document explains how to run the provided fetch and display
of images as per user query. The data of the images, are processed
and prebuilt as vectorized indices by a separate code which takes 
5 hours to run on my Macbook M2 Pro Max. I will share this already 
prepared data so that we dont need to run the data preparation code 
separately. Instead, we will read the prepared data and only 
display what the user asked for in the query.

Note: The data preparation code does not need a customer UI as it 
is a backend admin activity

------------------------------------------------------------
1. What this program does
------------------------------------------------------------

This program:
- Loads a pretrained AI model
- Converts a text query into a numeric representation
- Searches a prebuilt vector index of images
- Displays the most relevant images and their captions

You are NOT training any model.
You are only running an existing pretrained model and prepared data.

------------------------------------------------------------
2. What is a Python environment
------------------------------------------------------------
A Python environment is an isolated workspace that contains:
- A specific Python version
- Only the libraries needed for one project

Why this matters:
- Avoids breaking other projects
- Prevents library version conflicts
- Makes installation safer and reproducible

We can use Conda to manage Python environments.

------------------------------------------------------------
3. Create and activate the Python environment
------------------------------------------------------------

Open a terminal (Mac/Linux) or Anaconda Prompt (Windows).

Run the following commands exactly:

conda create -n visual-rag-v2 python=3.11 -y
conda activate visual-rag-v2

After activation, your terminal prompt should show:

(visual-rag-v2):

This means you are inside the correct environment.

------------------------------------------------------------
6. Required folder structure
------------------------------------------------------------

Create and following folder/directory structure in your harddisk 
or EC2and keep each item in the exact same place as show below:

project_root/
├── main.py
├── requirements.txt
├── README.txt
└── data/
    └── indexed_data/
        └── index/
            ├── faiss.index
            └── metadata.json

Important: 
- I will provide all these .py, .txt, .index and .json files 
as these created by a separate data processing code.

------------------------------------------------------------
4. Install required Python libraries
------------------------------------------------------------
After the above folder structure is ready and all files are
in their right place, go to the terminal and run

conda activate visual-rag-v2
pip install -r requirements.txt

This commands installs all necessary libraries.

------------------------------------------------------------
7. Running the program
------------------------------------------------------------

After:
- activating the environment
- installing dependencies
- verifying the folder structure

Run the script:

python main.py

------------------------------------------------------------
7. First run
------------------------------------------------------------

When the code runs for the first time, it can take 10-30 mins
depending on your hardware. This is because installing the libraries
does not automatically downloads the big underlying AI models 
such as CLIP (a few gb in size). It will be downloaded at first 
run. However, once downloaded, the 2nd query onwards it will 
take only a few seconds display the images as per the query.

------------------------------------------------------------
8. Changing the text query
------------------------------------------------------------

Inside the code, look for:

QUERY = "a room with a fan"

Change the text inside the quotes to whatever you want.

------------------------------------------------------------
8. Split the code
------------------------------------------------------------
Only the following portion of the code needs to run each time
the user as a new query. The part of the code before this is 
basically to load the model and necassary libraries so this must 
be done only once in each session. This saves 5-10 seconds of 
unnecessary reloading dependencies. So split the code accordingly
in your implementation.

TOP_K = 15
HYBRID_CANDIDATES = 300
QUERY = "a room with a fan"

if __name__ == "__main__":
    store = function_3(INDEX_DIR)
    logger.info("Loaded existing index.")
    results = function_4(store, QUERY, TOP_K)
    function_5(results, TOP_K)
