import io
import streamlit as st
from sidebar import add_logo
from PIL import Image
from streamlit_option_menu import option_menu
from sidebar import add_logo
from streamlit_extras.switch_page_button import switch_page
from create_body import kickoffTheCrew, query_huggingface

# Style options dictionary
style_options = {
    'Writer': ['Essays', 'Poem', 'Joke', 'Blog'],
    'Social': ['Funny', 'Formal', 'Friendly'],
    'Image': ["Abstract", "Cute", "Fantasy", "Futuristic", "Realistic", "Science Fiction", "Surreal", "Techno"]
}

# Setting the page configuration and title
st.set_page_config(page_title="Creative AI Content Generator", layout="wide")

#Menu
add_logo()
st.session_state.menu_option = option_menu(None, ["Home", "All", "Agent", 'Web', 'News', 'Create'], 
        icons=['house', 'globe2', "robot", 'search', 'newspaper', 'magic'], 
        menu_icon="cast", default_index=1, orientation="horizontal")

# Jump to selected page menu_option (not home since we are already here)
if st.session_state.menu_option in ("Home","Agent","Web"):
        switch_page(st.session_state.menu_option)

# Create title with search bar
from header import head
head("Snap 🪄 Content Generator", " ")

# Defining tab structure
tab1, tab2, tab3 = st.tabs(['✍️ Writer', '💬 Social', ' 🖼 Image'])

# Dictionary to keep track of the selected styles for each content type
selected_styles = {
    'Writer': [],
    'Social': [],
    'Image': []
}
# Function to decode the image from the API's binary response
def decode_image_from_response(content):
    return Image.open(io.BytesIO(content))


with tab1:
    prompt_column, result_column = st.columns(2)
    with prompt_column:
        st.subheader("Creative Writer ✍️")
        prompt_text = st.text_area("Enter the topic you want to write about", height=150)
        # Corrected: Ensure that the style selected is directly passed as a string
        selected_style = st.selectbox("Choose your style:", style_options['Writer'], key='WriterStyle')
        generate_button = st.button("Generate 🪄", key='GenerateWrite')
    with result_column:
        st.subheader("Your AI Written Creation")
        # Use st.empty() to create a placeholder for future content
        result_placeholder = st.empty()
        if generate_button:
            # Use the selected_style directly as it is already a string
            with st.spinner(f"Creating {selected_style}... Please wait."):
                # Pass the selected_style directly
                result = kickoffTheCrew(prompt_text, selected_style)
                # Update the placeholder with a scrollable container
                with result_placeholder.container():
                    st.markdown(f"### Style: {selected_style}")
                    # Use a container or expander to create a scrollable area
                    with st.expander("See Result", expanded=True):
                        st.write(result)  # This will be inside a scrollable expander
with tab2:
    st.write("Customize your Social")
    selected_styles['Social'] = st.multiselect("Choose your style:", style_options['Social'], key='Social')

with tab3:
    #Split the layout into two columns
    prompt_column, result_column = st.columns(2)
    with prompt_column:
        st.subheader("Customize your Image")
        prompt_text = st.text_area("Describe the scene", height=150)
        art_styles = st.multiselect("Choose a style", style_options['Image'], key='Image')
        generate_button = st.button("Generate 🪄", key='GenerateImage')
    with result_column:
        st.subheader("Your AI Artwork")
        if generate_button:
            with st.spinner("Creating Artwork... Please wait."):
                response_content = query_huggingface(prompt_text, art_styles)
                artwork_image = decode_image_from_response(response_content)
                st.image(artwork_image, use_column_width=True)
