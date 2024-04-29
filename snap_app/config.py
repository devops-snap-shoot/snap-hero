import streamlit as st

# AN exception will be raised if the secret is not found
#EXA
EXA_API_KEY = st.secrets["EXA_API_KEY"]
#OPENAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ORGANIZATION_ID = st.secrets["ORGANIZATION_ID"]
#SERPER
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
#Google
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GOOGLE_CSE_ID = st.secrets["GOOGLE_CSE_ID"]
#TAVILY
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
