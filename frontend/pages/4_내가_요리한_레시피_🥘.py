import streamlit as st

from common import init, page_header 
from user_history import user_history_page 
#from pages.recommendation import back_to_home_container

def back_to_home_container():
    with st.container(border=True):
        cols = st.columns([3,2,2])
        with cols[1]:
            st.write('로그인이 필요합니다.')
        cols = st.columns([4,2.5,3])
        with cols[1]:
            st.link_button('메인페이지로 >>', st.session_state.url_main, type='primary')


if not st.session_state.is_authenticated:
    page_header()
    back_to_home_container()
else:
    page_header()
    user_history_page()
