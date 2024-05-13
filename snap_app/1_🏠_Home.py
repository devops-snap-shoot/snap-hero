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
from serpapi import GoogleSearch


# Function to set up the Streamlit page configuration
def setup_page_config():
    st.set_page_config(page_title="Snap", page_icon="🤖")

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
        f'{"Hello again"}</h1>',
        unsafe_allow_html=True
    )
    st.header(' ', divider='rainbow')
    st.caption('Explore, Create, Share...')

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
    # Change from text_input to text_area for multiline input
    search_query = st.text_area(" ", placeholder="Tell me what's on your mind...", key="search_input", height=100)
    st.session_state.query = search_query.strip()
    left_space, col1, col2, right_space = st.columns([1, 1, 1, 1])
    if col1.button("🧭 Explore"):
        if search_query.strip():
            intent = get_intent(search_query.strip(), client)
            if intent == "agent":
                switch_page("GPT")
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
     
def fetch_news(number_of_news=2, type_of_news='trending', country_code='us'):
    api_key = st.secrets["SERPAPI_KEY"]
    news_items = []

    if type_of_news == 'trending':
        # Fetch trending news using the Google Trends API
        params = {
            "engine": "google_trends_trending_now",
            "frequency": "realtime",
            "api_key": api_key
        }
        url = "https://serpapi.com/search"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("realtime_searches", [])[:number_of_news]:
                if 'articles' in item:
                    article = item['articles'][0]
                    news_items.append({
                        'title': article.get('title', 'No title available'),
                         'image_url': article.get('thumbnail', None),
                        'link': article.get('link', '#')
                    })
    else:
        # Fetch news using the Google News API
        params = {
            "engine": "google_news",
            "q": "latest news",
            "hl": "en",
            "gl": country_code,
            "api_key": api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])
        for item in news_results[:number_of_news]:
            news_items.append({
                'title': item.get('title', 'No title available'),
                'image_url': item.get('thumbnail', None),
                'link': item.get('link', '#'),
            })

    return news_items


def display_news(news_list, title):
    st.markdown(f"<h2 style='color: gray; font-size: 16px; margin-bottom: 10px;'>{title}</h2>", unsafe_allow_html=True)
    for news in news_list:
        with st.container():
            col1, col2 = st.columns([1, 5])  # Adjust column ratios if necessary
            with col1:
                image = download_and_resize_image(news['image_url'])
                if image:
                    st.image(image, width=100, use_column_width=True)
                else:
                    st.write("Image not available")  # Provide feedback if no image is available
            with col2:
                # Wrap the title in an anchor tag to make it clickable
                st.markdown(f"""
                    <a href='{news['link']}' target='_blank' style='text-decoration: none;'>
                        <p style='font-size: 18px; font-weight: bold; overflow: hidden; display: -webkit-box; 
                        -webkit-line-clamp: 2; -webkit-box-orient: vertical; color: black;'>
                            {news['title']}
                        </p>
                    </a>
                """, unsafe_allow_html=True)
            st.markdown("---")  # Add a divider after each news item

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

# The main function wrapping all actions
def main():
    setup_page_config()
    initialize_state()
    hide_streamlit_format()
    client = create_openai_client()
    image_base64 = get_image_base64()
    create_header(image_base64)
    create_search_and_create_buttons(client)
    
    col1, col2 = st.columns(2)
    with col1:
        trending_news = fetch_news(number_of_news=2, type_of_news='trending')
        display_news(trending_news , "Trending")
    with col2:
        local_news = fetch_news(number_of_news=2, type_of_news='local', country_code='cl')
        display_news(local_news, "News")
    

    game_of_the_day()
    
   # Call the function to render AdSense code
    # adsense_code()

if __name__ == "__main__":
    main()
