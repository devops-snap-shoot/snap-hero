
import os
import streamlit as st
import snapsettings
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from openai import OpenAI

st.set_page_config(page_title="Snap", page_icon = "🤖", initial_sidebar_state="collapsed")

openai_api_key = st.secrets["OPENAI_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

# Create the OpenAI API client
client = OpenAI(
    organization='org-S6hG2xydQF8XwcexPJtyE0q3',
)

#define text_search global
snapsettings.last_query=""
message =""

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

#simulate nav bar with buttons on top
with stylable_container(
    key="🌎All",
    css_styles="""
        button {
            background-color: transparent;
            color: gray;
            border-radius: 25px;
            border-color: transparent;
        }
        """,
):
    cc = st.columns(6)
    with cc[0]:
        if st.button("🌎All"):
            switch_page("All")  # This is where the page gets switched
    with cc[1]:
        if st.button("🤖Agent"):
            message ="🤖 Agent will be soon!!!" # This is where the page gets switched
    with cc[2]:
        if st.button("🔍Web"):
            switch_page("Web")  # This is where the page gets switched
    with cc[3]:
        if st.button("🗞News"):
             message ="🗞️ News will be soon!!!"# This is where the page gets switched
    with cc[5]:
        if st.button("✨Create"):
             message ="✨Create will be soon!!!"
       
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
snapsettings.text_query = search_query.strip()

col1, col2 = st.columns(2)
emptycol1, col1, col2, emptycol2 = st.columns([2, 2, 2, 2])
if col1.button("🤖 Search"):
    if search_query.strip():
        if (get_intent(search_query.strip())=="agent"):
            st.warning(f"🤖 Agent will be soon!!!")
             #switch_page("Agent")
        else: #if user don't ask for agent then go to search page
            switch_page("All")
        
    else:
            st.error("Please provide the search query.")     
if col2.button("✨ Create"):
        #switch_page("Create")
        st.warning(f"✨ Create will be soon!!!")
if message != "":
    st.warning(message)
    
    