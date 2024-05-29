from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
import streamlit as st
from streamlit_option_menu import option_menu
from sidebar import add_logo
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Snap", page_icon ="🧭")

openai_api_key = st.secrets["OPENAI_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]
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
# if dont exist do nothing
if 'search_input' not in st.session_state:
    st.session_state.search_input = st.session_state.query  
if 'message' not in st.session_state:
    message = st.session_state.message
    
#Menu
add_logo()

# Create title with search bar
from header import head
head("Discover", " ")


# Function to perform the search operation

def perform_search(query):
    try:
        with st.spinner('Looking for information...'): 
            # Initialize the ChatOpenAI module, load the Google Serper API tool, TavilySearchResults tool, and run the search query using a React agent
            llm = ChatOpenAI(temperature=0.3, model_name="gpt-4", streaming=True, verbose=True)
            
            # Initialize the TavilySearchResults tool separately
            tavily_tool = TavilySearchResults(max_results=1)
            
            # Load other tools
            tools = load_tools(["google-serper"], llm)
            
            # Add the TavilySearchResults tool to the list of tools
            tools.append(tavily_tool)
            
            # Ensure to use the correct endpoint for a chat model
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose=True)
            
            response = agent.run(query)
            st.success(response)
            
            # Show the top X relevant web sites using Google Serper API
            search = GoogleSerperAPIWrapper()
            result_dict = search.results(query)
            
            if not result_dict['organic']:
                st.error(f"No search results for: {query}.")
            else:
                cols = st.columns(2)
                for i, (col, item) in enumerate(zip(cols*2, result_dict['organic'])):
                    with col:
                        truncated_link = item['link'][:50] + '...' if len(item['link']) > 30 else item['link']
                        st.success(f"Title: {item['title']}\n\n{item['snippet']}\n\nLink: {truncated_link}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Full traceback:")
        st.exception(e)
        
# Handle the text input and the button
col1, col2 = st.columns([5, 1])

with col1:
    new_input = st.text_input("Search", value=st.session_state.search_input if st.session_state.search_input else "", placeholder="Search anything...", label_visibility="collapsed")
    if new_input:
        st.session_state.search_input = new_input  # Update session state with new input
        st.session_state.query = new_input  # Keep text_query in sync with the user input

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
if st.session_state.query and not output_print:
    if new_input:
        perform_search(new_input)
if st.session_state.message != "":
    st.warning(st.session_state.message)
    