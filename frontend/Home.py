# Temporal Entrypoint
import streamlit as st

from utils import page_header 

# define session-page
def home():
    page_header()

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

home()
