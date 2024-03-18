import time, math
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests

import streamlit as st
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container
from st_supabase_connection import SupabaseConnection
from st_login_form import login_form
from streamlit_login_auth_ui.widgets import __login__

# import sys
# sys.path.append('frontend')
from pages import result_page_2, recommendation_page, main_page_2, signin_page, user_history_page, main_page

global api_prefix
api_prefix = "http://localhost:8000/"

# , signin_page, login_page, signin_page_2, signin_page_3, main_page_2
menu_titles = ["house", "🛒이번주 장바구니 추천", "😋내가 요리한 레시피", "🔎취향저격 레시피", "Log In / 회원가입"]

st.set_page_config(layout="wide")

# 세션 초기화
if 'page_info' not in st.session_state:
    st.session_state['page_info'] = 'home'

# 로그인되어 있다고 가정
def init():
    st.session_state.user = 1 
    st.session_state.is_authenticated = True

# 로그인 상태 초기화
init()


# page_info 설정
st.session_state['page_info'] = 'home'

app_title = "🛒 나만의 식량 바구니"
menu_titles = ["house", "🛒이번주 장바구니 추천", "😋내가 요리한 레시피", "🔎취향저격 레시피", "Log In / 회원가입", "MainPage-2", "User history"]
################

################
# body -> main -> sub
container1 = st.container(border=True)
with container1:
    cols = st.columns([1,2])
    with cols[0]:
        st.markdown(f"<h4> {app_title} </h4>", unsafe_allow_html=True)
    with cols[1]:
        seg = sac.segmented(
            items=[
                sac.SegmentedItem(icon=menu_titles[0]),
                sac.SegmentedItem(label=menu_titles[1]),
                sac.SegmentedItem(label=menu_titles[2]),
                sac.SegmentedItem(label=menu_titles[3]),
                sac.SegmentedItem(label=menu_titles[4]),
                sac.SegmentedItem(label=menu_titles[5]),
                sac.SegmentedItem(label=menu_titles[6]),
            ], align='center', use_container_width=True,
        )

    container2 = st.container(border=True)
    with container2:
        if seg == menu_titles[1]:
            # 🛒이번주 장바구니 추천
            container3 = st.container(border=True)
            with container3:
                st.markdown(f"<h4 style='text-align: center;'>{menu_titles[1]}</h4>", unsafe_allow_html=True)
            
                if 'page_info' not in st.session_state:
                    st.session_state['page_info'] = 'recommend'
                    recommendation_page()

                if st.session_state['page_info'] == 'result_page_1':
                    result_page_2()
                
        elif seg == menu_titles[2]:
            # 😋내가 요리한 레시피
            st.session_state['page_info'] = 'recommend_history'
            main_page_2()
        elif seg == menu_titles[3]:
            st.session_state['page_info'] = 'recommend_history'
            main_page_2()
        elif seg == menu_titles[4]:
            # 로그인 / 회원가입
            signin_page()
        elif seg == menu_titles[5]:
            # MainPage_2
            # main_page_2()
            
            st.session_state['page_info'] = "result_page_2" 
            result_page_2()
        elif seg == menu_titles[6]:
            
            # show UserHistoryPage
            st.session_state['page_info'] = 'user_history'
            user_history_page()
        else :
            # Home
            main_page()