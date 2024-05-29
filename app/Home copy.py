import os
from openai import OpenAI
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from openai import OpenAI 
from streamlit_option_menu import option_menu
from header import img_to_base64
from sidebar import add_logo

# Streamlit initialize query and message to blank
# If query or message already exist, don't do anything
if 'query' not in st.session_state:
	st.session_state.query = ""
if 'message' not in st.session_state:
	st.session_state.message = ""

# Create the OpenAI API client
client = OpenAI(
    organization=st.secrets["ORGANIZATION_ID"],
)

st.set_page_config(page_title="Snap", page_icon = "🤖", initial_sidebar_state="collapsed")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")
img_path = os.path.join(assets_dir, "snap-logo.png")

# Now use img_path 
image_base64 = img_to_base64(img_path)

# Create header with image and text 
# st.logo(img_path)  # will be soon

add_logo(image_base64)


#Menu 
st.session_state.menu_option = option_menu(None, ["Home", "All", "Agent", 'Web', 'News', 'Create'], 
        icons=['house', 'globe2', "robot", 'search', 'newspaper', 'magic'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

# Jump to selected page menu_option (not home since we are already here)
if st.session_state.menu_option in ("All","Agent","Web","Create"):
        switch_page(st.session_state.menu_option)

# Adding hide header foother
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Create title 
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

def get_intent(user_query):
    prompt = (
        "You will be provided with a question, and your task  is to classify its intent as search or agent. Only respond with either 'search' if the user is looking for internet information or 'agent' if the user wants to ask or talk to an agent like ChatGPT, nothing else."
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
    return assistant_response


#titulos pagina inicial            
st.markdown(
    f'<h1 style="display: inline;">'
    f'<img src="data:image/png;base64,{image_base64}" style="vertical-align:middle; margin-right: 10px;" width="40" height="40"/>'
    f'{"Snap-Shoot"}</h1>',
    unsafe_allow_html=True
    )
st.header(' ', divider='rainbow')
st.caption('Explore, Create, Share...')
search_query =""
search_query = st.text_input("Search", placeholder="Search or Ask...", key="search_input", label_visibility="collapsed")
st.session_state.query = search_query.strip()

#Botones
col1, col2 = st.columns(2)
emptycol1, col1, col2, emptycol2 = st.columns([2, 2, 2, 2])
if col1.button("🤖 Search"):
    if search_query.strip():
        if (get_intent(search_query.strip())=="agent"):
            switch_page("Agent")
        else: #if user don't ask for agent then go to search page
            switch_page("All")
        
    else:
            st.error("Please provide the search query.")     
if col2.button("✨ Create"):
        switch_page("Create")
if st.session_state.message != "":
    st.warning(st.session_state.message)
    
if st.session_state.menu_option in ("News"):
        # Display a warning message since pages are not ready
        st.warning(f"{st.session_state.menu_option} will be soon!!")
