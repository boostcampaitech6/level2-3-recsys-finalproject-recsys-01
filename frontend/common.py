import streamlit as st

def init():
    st.session_state.is_authenticated = False 

def set_logout():
    st.session_state.user = None
    st.session_state.is_authenticated = False 

def set_login():
    st.session_state.user = 'judy123' 
    st.session_state.is_authenticated = True

def login_button():
    if st.session_state.is_authenticated:
        login_button = st.button(f"{st.session_state.user}님 | 로그아웃", on_click=set_logout)
    else:
        login_button = st.button(f"회원가입 | 로그인", on_click=set_login)
    return login_button

def page_header():
    cols = st.columns([8,3])
    with cols[0]:
        st.header('나만의 식량 바구니')
    with cols[-1]:
        login_button()
    button_css()

def button_css():
    st.markdown(
        """<style>
        button[kind="secondary"] {
            border: none !important;
              }
        div[data-testid="stMarkdownContainer"] p {
            font-size: 14px;/* !important;*/
        }
            </style>""",
        unsafe_allow_html=True,
    )
