import os
import subprocess
import nltk

# Ensure NLTK packages are downloaded
nltk_packages = ['wordnet', 'pros_cons', 'reuters']
for package in nltk_packages:
    nltk.download(package)

# Get the port from the environment
port = os.environ.get('PORT', 8501)

# Run the Streamlit app
command = f"streamlit run home.py --server.port={port}"
subprocess.run(command, shell=True)
