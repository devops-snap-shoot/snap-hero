from pytrends.request import TrendReq
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def fetch_trending_searches():
    """Fetch the latest trending searches from Google Trends."""
    # You can change the location parameter as needed, 'united_states' can be changed to other regions
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    return trending_searches_df[0].tolist()

def download_and_display_image(search_term):
    """Download and display an image related to the search term using Bing Image Search API or similar."""
    # Here you can use an image API of your choice to fetch images related to the search term
    # Placeholder for Bing Image Search or other service
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": "your_bing_api_key_here"}
    params = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        image_results = response.json()
        first_image_url = image_results["value"][0]["thumbnailUrl"]
        response = requests.get(first_image_url)
        img = Image.open(BytesIO(response.content))
        return img
    else:
        return None

def main():
    st.title("Google Trends - Real-Time Search Trends")
    trending_searches = fetch_trending_searches()

    st.header("Top Trending Searches")
    for term in trending_searches:
        st.subheader(term)
        image = download_and_display_image(term)
        if image:
            st.image(image, caption=term)

if __name__ == "__main__":
    main()
