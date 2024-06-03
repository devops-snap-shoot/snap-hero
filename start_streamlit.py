import os
import subprocess

port = os.environ.get('PORT', 8501)
command = f"streamlit run snap_app/1_🏠_Home.py --server.port={port}"
subprocess.run(command, shell=True)
