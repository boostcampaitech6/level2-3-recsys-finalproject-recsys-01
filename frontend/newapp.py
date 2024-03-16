import streamlit as st

from common import init, page_header 
from basket_signup import signup_container
from basket_login import login_container

def home():
    page_header()

def home2():
    page_header()
    st.write('login 됨')

def login():
    page_header()
    login_container()

def signup():
    page_header()
    signup_container()


if ('is_authenticated' not in st.session_state) and ('page_info' not in st.session_state):
    init()

if (not st.session_state.is_authenticated) and (st.session_state.page_info == 'home'):
    home()
elif (not st.session_state.is_authenticated) and (st.session_state.page_info == 'signup'):
    signup()
elif (not st.session_state.is_authenticated) and (st.session_state.page_info == 'login'):
    login()
elif (st.session_state.is_authenticated) and (st.session_state.page_info == 'home2'):
    home2()

