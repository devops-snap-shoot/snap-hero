import os
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from openai import OpenAI
from header import img_to_base64
from sidebar import add_logo
import streamlit.components.v1 as components
from footer import adsense_code, load_game


# Function to set up the Streamlit page configuration
def setup_page_config():
    st.set_page_config(page_title="Snap", page_icon="🤖", initial_sidebar_state="collapsed")

# Function to initialize the session state
def initialize_state():
    if 'query' not in st.session_state:
        st.session_state.query = ""
    if 'message' not in st.session_state:
        st.session_state.message = ""

# Function to create the OpenAI API client
def create_openai_client():
    return OpenAI(organization=st.secrets["ORGANIZATION_ID"])

# Function to get the base64 string of the image
def get_image_base64():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    img_path = os.path.join(assets_dir, "snap-logo.png")
    return img_to_base64(img_path)

# Function to create the header with image and menu
def create_header_and_menu(image_base64):
    add_logo()
    st.session_state.menu_option = option_menu(None, ["Home", "All", "Agent", 'Web', 'News', 'Create'], 
            icons=['house', 'globe2', "robot", 'search', 'newspaper', 'magic'], 
            menu_icon="cast", default_index=0, orientation="horizontal")

    # Menu option selection
    if st.session_state.menu_option in ("All", "Agent", "Web", "Create"):
        switch_page(st.session_state.menu_option)

    # Display the header
    st.markdown(
        f'<h1 style="display: inline;">'
        f'<img src="data:image/png;base64,{image_base64}" style="vertical-align:middle; margin-right: 10px;" width="40" height="40"/>'
        f'{"Snap-Shoot"}</h1>',
        unsafe_allow_html=True
    )
    st.header(' ', divider='rainbow')
    st.caption('Explore, Create, Share...')

# Function to hide the default Streamlit format
def hide_streamlit_format():
    hide_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_format, unsafe_allow_html=True)

# Function to classify the intent of the user query
def get_intent(user_query, client):
    prompt = (
        "You will be provided with a question, and your task is to classify its intent as search or agent. "
        "Only respond with either 'search' if the user is looking for internet information or 'agent' if the user wants to "
        "talk to an agent like ChatGPT, nothing else."
    )
    response = client.chat.completions.create(
        model="gpt-4",
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
    search_query = st.text_input("Search", placeholder="Search or Ask...", key="search_input", label_visibility="collapsed")
    st.session_state.query = search_query.strip()
    left_space, col1, col2, right_space = st.columns([1, 1, 1, 1])
    if col1.button("🤖 Search"):
        if search_query.strip():
            intent = get_intent(search_query.strip(), client)
            if intent == "agent":
                switch_page("Agent")
            else: # if user didn't ask for an agent then go to search page
                switch_page("All")
        else:
            st.error("Please provide the search query.")     
    if col2.button("✨ Create"):
            switch_page("Create")

    # Handle display of warning messages
    if st.session_state.message:
        st.warning(st.session_state.message)
    if st.session_state.menu_option == "News":
        # Display a warning message since the News page is not ready
        st.warning(f"{st.session_state.menu_option} will be soon!!")

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

# The main function wrapping all actions
def main():
    setup_page_config()
    initialize_state()
    client = create_openai_client()
    image_base64 = get_image_base64()
    create_header_and_menu(image_base64)
    hide_streamlit_format()
    create_search_and_create_buttons(client)
    game_of_the_day()
    #Call the function to render AdSense code
    #adsense_code()


if __name__ == "__main__":
    main()

