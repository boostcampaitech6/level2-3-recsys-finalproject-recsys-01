# Temporal Entrypoint
import streamlit as st

from utils import page_header 

# define session-page
def home():
    page_header(False, None)

# 세션 초기화
if 'page_info' not in st.session_state:
    st.session_state['page_info'] = 'home'
st.session_state['page_info'] = 'home'

# 이전 추천 목록 조회
home()
