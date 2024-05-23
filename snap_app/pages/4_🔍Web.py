import os
from langchain.llms import OpenAI
import openai
import snapsettings
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.agents import load_tools, initialize_agent
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Snap", page_icon ="🤖", initial_sidebar_state="collapsed")

openai_api_key = st.secrets["OPENAI_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

# Adding hide header foother
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

output_print = False #nothing print yet
# Initialize session state variables if they don't exist
if 'search_input' not in st.session_state:
    st.session_state.search_input = snapsettings.text_query  # Initialize with text_query if it exists

message =""
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

# Create columns and All button
    cc = st.columns(6)
    with cc[0]:
        if st.button("🌎All"):
            switch_page("All")  # This is where the page gets switched
    with cc[1]:
        if st.button("🤖Agent"):
            mensaje ="🤖 Agent will be soon!!!" # This is where the page gets switched
    with cc[2]:
        if st.button("🔍Web"):
            switch_page("Web")  # This is where the page gets switched
    with cc[3]:
        if st.button("🗞News"):
             mensaje ="🗞️ News will be soon!!!"# This is where the page gets switched
    with cc[5]:
        if st.button("✨Create"):
             mensaje ="✨Create will be soon!!!"

# Create title with search bar
from header import head
head("Snap🌎All", " ")

# Function to perform the search operation
def perform_search(query):
    try:
        with st.spinner('Please wait...'): 
            # Initialize the OpenAI module, load the Google Serper API tool, and run the search query using an agent
            llm = ChatOpenAI(temperature=0.5, model_name="gpt-4",verbose=True)
            tools = load_tools(["google-serper"], llm)
            # Ensure to use the correct endpoint for a chat model
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", handle_parsing_errors=True, verbose=True)
            result = agent.run(query)
            st.success(result)
            
            # Show the top X relevant web sites using Google Serper API
            search = GoogleSerperAPIWrapper()
            result_dict = search.results(query)  # Use query parameter
            if not result_dict['organic']:
                st.error(f"No search results for: {query}.")  # Use query parameter
            else:
                cols = st.columns(2)  # Create two columns
                
                for i, (col, item) in enumerate(zip(cols*2, result_dict['organic'])):  # Loop through 2x2 grid
                    with col:
                        # Truncate the link after 50 characters and add "..." if needed
                        truncated_link = item['link'][:50] + '...' if len(item['link']) > 30 else item['link']

                        st.success(f"Title: {item['title']}\n\n{item['snippet']}\n\nLink: {truncated_link}")

    except Exception as e:
        st.exception(f"An error occurred: {e}")

# Handle the text input and the button
col1, col2 = st.columns([5, 1])

with col1:
    new_input = st.text_input("Search", value=st.session_state.search_input if st.session_state.search_input else "", placeholder="Search anything...", label_visibility="collapsed")
    if new_input:
        st.session_state.search_input = new_input  # Update session state with new input
        snapsettings.text_query = new_input  # Keep text_query in sync with the user input

with col2:
    button_press = st.button("🔍")

# The echo logic
if button_press:
    if not new_input:
        st.error("Please provide the search query.")
    else:
        perform_search(new_input)
        output_print = True

# The echo logic for initial load with session state
if snapsettings.text_query and not output_print:
    if new_input:
        perform_search(new_input)
if message != "":
    st.warning(message)