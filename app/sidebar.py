import os
import streamlit as st
from header import img_to_base64


#def sidebar():
#    with st.sidebar:

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")
img_path = os.path.join(assets_dir, "snap-logo.png")

# Now use img_path 
image_base64 = img_to_base64(img_path)

        
def add_logo():
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{image_base64}");
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 10px 80px;  /* Position logo at top left with some padding */
                background-size: 40px 40px;     /* Logo size */
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "Snap-Shoot";
                font-size: 28px;               /* Text size larger */
                color: gray;                   /* Text color gray */
                position: absolute;
                top: 76px;                     /* Vertically center the text with the logo */
                left: 60px;                    /* Text aligned to the left, spaced from the logo */
                display: block;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


