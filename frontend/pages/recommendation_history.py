import streamlit as st

from common import init, page_header 
from recommendation_history import recommendation_history_page 
from pages.recommendation import back_to_home_container

if not st.session_state.is_authenticated:
    page_header()
    back_to_home_container()
else:
    page_header()
    recommendation_history_page()
