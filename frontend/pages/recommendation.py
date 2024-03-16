import streamlit as st

from common import init, page_header 
from newapp import recommendation
from result_page import result_page
from main import welcome_container
#from recommendation import recommendation_page

if 'is_authenticated' not in st.session_state:
    init()
    print('page_recommendation')
    st.session_state.page_info = 'recommendation'

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

elif st.session_state.get('is_authenticated', False) and (st.session_state.get('page_info', '-') == 'result_page_1'):
    result_page()

else:
    recommendation()

