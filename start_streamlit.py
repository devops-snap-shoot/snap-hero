import os
import subprocess
import nltk

# Download NLTK packages
nltk_packages = ['wordnet', 'pros_cons', 'reuters']
for package in nltk_packages:
    nltk.download(package)

# Get the port from the environment
port = os.environ.get('PORT', 8501)

# Run the Streamlit app
command = f"streamlit run snap-app/1_🏠_Home.py --server.port={port}"

subprocess.run(command, shell=True)