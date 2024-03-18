import streamlit as st

from common import init, page_header 
from basket_signup import signup_container
from basket_login import login_container
from main import main_page
from main_2 import main_page_2
from signinpage_2 import choose_food_page

def home():
    page_header()
    main_page()

def home2():
    page_header()
    main_page_2()

def login():
    page_header()
    login_container()

def signup():
    page_header()
    signup_container()

def choose_food():
    page_header()
    choose_food_page()

if ('is_authenticated' not in st.session_state) and ('page_info' not in st.session_state):
    init()

if (not st.session_state.get('is_authenticated', False)) and (st.session_state.get('page_info', '-') == 'signup'):
    signup()
elif (not st.session_state.get('is_authenticated', False)) and (st.session_state.get('page_info', '-') == 'login'):
    login()
elif not st.session_state.get('is_authenticated', False):
    home()
elif st.session_state.get('is_authenticated', False):
    if st.session_state['token']['is_first_login']:
        choose_food()
    else:
        home2()

print(st.session_state.is_authenticated)
print(st.session_state.page_info)
