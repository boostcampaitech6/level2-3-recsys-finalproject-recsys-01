import streamlit as st

from common import init, page_header, back_to_home_container
from result_page import result_page
from main import welcome_container
from recommendation import recommendation_page

def recommendation():
    page_header()
    recommendation_page()

if 'is_authenticated' not in st.session_state:
    init()
    st.session_state.page_info = 'recommendation'

if not st.session_state.is_authenticated:
    page_header()
    back_to_home_container()
elif st.session_state.get('is_authenticated', False) and (st.session_state.get('page_info', '-') == 'result_page_1'):
    result_page()
elif st.session_state.get('is_authenticated', False) and (st.session_state.get('page_info', '-') == 'result_page_2'):
    result_page()
else:
    recommendation()