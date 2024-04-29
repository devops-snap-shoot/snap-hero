# footer.py
import os
import streamlit as st
import streamlit.components.v1 as components

# Function to load and display the game
def load_game():
    # Relative path to the 'snap_game.html' file
    relative_path = 'snap_game.html'
    file_path = os.path.join(os.path.dirname(__file__), relative_path)

    try:
        # Read the content of the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        # Use the 'html' method to display the HTML page within the Streamlit app
        components.html(html_content, height=600, scrolling=False)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    
def adsense_code():
    # The URL where your ads.html is served locally
    ads_url = "http://localhost:8000/ads.html"  # Replace with the correct port and path

    # Use an iframe to include the external HTML that contains AdSense
    components.html(f'<iframe src="{ads_url}" width="100%" height="90" style="border:none;"></iframe>', height=90)
