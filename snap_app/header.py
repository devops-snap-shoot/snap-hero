import os
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import base64

# Convert image to base64
import base64
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")
img_path = os.path.join(assets_dir, "snap-logo.png")

# Function to convert image to base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Now use img_path 
image_base64 = img_to_base64(img_path)

# Create header with image and text 

def head(header_text, caption_text):
    st.markdown(
    f'<h3 style="display: inline;">'
    f'<img src="data:image/png;base64,{image_base64}" style="vertical-align:middle; margin-right: 5px;" width="30" height="30"/>'
    f'{header_text}</h2>',
    unsafe_allow_html=True
    )
    if caption_text:
        st.caption(caption_text)
    
        


