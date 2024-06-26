"""
    Streamlit UI for Snap.
    Structure:
        - A text field for initial question
        -aSide Bar for Page navigation
        - A container section with columns for displaying trendy and personal search results
        - Each search result is a card with an image, title, date, and a button to see more
        - The button opens the original article in a new tab
    Note:
        It might take a few seconds to load the images, because they are downloaded from the web.
"""
import os
from io import BytesIO
import requests
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from openai import OpenAI
from header import img_to_base64
from sidebar import add_logo
from PIL import Image
from footer import load_game

import pathlib
from bs4 import BeautifulSoup
import logging
import shutil

# Function to initialize the session state
def initialize_state():
    if 'query' not in st.session_state:
        st.session_state.query = ""
    if 'message' not in st.session_state:
        st.session_state.message = ""

# Function to set up the Streamlit page configuration
def setup_page_config():
    st.set_page_config(page_title="Snap", page_icon="🤖")


# Function to create the OpenAI API client
def create_openai_client():
    return OpenAI(organization=st.secrets["ORGANIZATION_ID"])

# Function to get the base64 string of the image
def get_image_base64():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    img_path = os.path.join(assets_dir, "snap-logo.png")
    return img_to_base64(img_path)

# Function to hide the default Streamlit format
def hide_streamlit_format():
    hide_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_format, unsafe_allow_html=True)

# Function to create the header with image and menu
def create_header(image_base64):
    add_logo()
   
    # Display the header
    st.markdown(
        f'<h1 style="display: inline;">'
        f'<img src="data:image/png;base64,{image_base64}" style="vertical-align:middle; margin-right: 10px;" width="40" height="40"/>'
        f'{"Hello"}</h1>',
        unsafe_allow_html=True
    )
    st.header(' ', divider='rainbow')
    st.caption('Explore, Create, Share...')

# Function to classify the intent of the user query
def get_intent(user_query, client):
    prompt = (
        "You will be provided with a question, and your task is to classify its intent as search or agent. "
        "Only respond with either 'search' if the user is looking for internet information or use a simple word of name, or say  'agent' if the user wants to "
        "talk to an agent like ChatGPT or the question start whith someting like they want to chat or talk like: I want to know or What, tell me about, if you are unsure just say search nothing else."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )
    # Accessing the assistant's response from the ChatCompletion object
    assistant_response = response.choices[0].message.content
    return assistant_response.strip()

# Function to create the search and create buttons and handle their actions
def create_search_and_create_buttons(client):
    # Change from text_input to text_area for multiline input
    search_query = st.text_area(" ", placeholder="Tell me what's on your mind...", key="search_input", height=100)
    st.session_state.query = search_query.strip()
    left_space, col1, col2, right_space = st.columns([1, 1, 1, 1])
    if col1.button("🧭 Explore"):
        if search_query.strip():
            intent = get_intent(search_query.strip(), client)
            if intent == "search":
                switch_page("Explore")
            else:  # if user didn't ask for an agent then go to search page
                switch_page("GPT")
        else:
            st.error("Please provide the search query.")
    if col2.button("✨ Create "):
            switch_page("Create")

def download_and_resize_image(url):
    if not url:
        st.write("No image URL provided.")
        return None  # Early exit if no URL is provided

    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize using high-quality downscaling
            return img
        else:
            st.write(f"Failed to download image. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.write(f"An error occurred while downloading or resizing the image: {str(e)}")
        return None
               
#Game Section
def game_of_the_day():
    # Allocate three columns with a ratio that pushes the 'Game of the Day' button to the right
    
    if st.button('🕹 Game of the Day'):
        load_game()
        # Once the game is loaded, the following buttons will be displayed
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Play Again"):
                load_game()
        with col2:
            if st.button("Close"):
                st.experimental_rerun()  # Rerun to reload the home screen
                
# AddSense Section
import pathlib
import shutil
import logging
from bs4 import BeautifulSoup
import streamlit as st


def adsense_code():
    adsense_url = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
    GA_AdSense = """
      <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8155652268489082"
     crossorigin="anonymous"></script>
      <script>
          (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    """

    # Insert the script in the head tag of the static template inside your virtual environment
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find('script', src=adsense_url):
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  
        else:
            shutil.copy(index_path, bck_index)  
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_AdSense)
        index_path.write_text(new_html)


# The main function wrapping all actions
def main():
    initialize_state()
    setup_page_config()
    hide_streamlit_format()
    client = create_openai_client()
    image_base64 = get_image_base64()
    create_header(image_base64)
    create_search_and_create_buttons(client)
    
    # Call the function to render the game of the day 
    game_of_the_day()
    
   # Call the function to render AdSense code
    adsense_code()

if __name__ == "__main__":
    main()
