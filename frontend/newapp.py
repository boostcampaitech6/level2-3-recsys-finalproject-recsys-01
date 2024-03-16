import streamlit as st

from common import init, page_header 
from basket_signup import signup_container
from basket_login import login_container
from main import main_page
from recommendation import recommendation_page

def home():
    page_header()
    main_page()

def home2():
    page_header()
    st.write('login 됨')

def login():
    page_header()
    login_container()

def signup():
    page_header()
    signup_container()

def recommendation():
    page_header()
    recommendation_page()

if ('is_authenticated' not in st.session_state) and ('page_info' not in st.session_state):
    init()

value = st.session_state.get('key', 'default_value')
if (not st.session_state.get('is_authenticated', False)) and (st.session_state.get('page_info', '-') == 'home'):
    home()
elif (not st.session_state.get('is_authenticated', False)) and (st.session_state.get('page_info', '-') == 'signup'):
    signup()
elif (not st.session_state.get('is_authenticated', False)) and (st.session_state.get('page_info', '-') == 'login'):
    login()
elif st.session_state.get('is_authenticated', False) and (st.session_state.get('page_info', '-') == 'home2'):
    home2()

