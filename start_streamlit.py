import os
import subprocess

# Call the NLTK download script
subprocess.run("python download_nltk_data.py", shell=True)

# Get the port from the environment
port = os.environ.get('PORT', 8501)

# Run the Streamlit app
command = f"streamlit run home.py --server.port={port}"
subprocess.run(command, shell=True)
