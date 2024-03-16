import random, string

import streamlit as st
import streamlit_antd_components as sac

random_chars = lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=5))

def init():
    print('init!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    st.session_state.is_authenticated = False 
    st.session_state.page_info = 'home'
    st.session_state.url_prefix = 'http://localhost:8000'
    st.session_state.url_main = 'http://175.45.194.96:8503/'

def set_logout_page():
    st.session_state.is_authenticated = False 
    st.session_state.page_info = 'home'

def set_login_page():
    st.session_state.page_info = 'login'

def set_signup_page():
    st.session_state.page_info = 'signup'
    print('signup_page')
    print(st.session_state.page_info)

def login_button():
    cols = st.columns(2)
    if st.session_state.is_authenticated:
        with cols[0]:
            st.write(f"{st.session_state.token['user_id']}님")
        with cols[1]:
            st.button(f"로그아웃", on_click=set_logout_page, key=f'logout_{st.session_state.page_info}_{random_chars()}')

    else:
        with cols[0]:
            st.button(f"회원가입", on_click=set_signup_page, key=f'signup_{st.session_state.page_info}_{random_chars()}')
        with cols[1]:
            st.button(f"로그인", on_click=set_login_page, key=f'login_{st.session_state.page_info}_{random_chars()}')
    return login_button

def page_header():
    cols = st.columns([7,3])
    with cols[0]:
        # st.header('나만의 식량 바구니')
        st.markdown(
            f'<h2><a href="{st.session_state.url_main}" target="_self" class="black-link">나만의 식량 바구니</a></h2>', 
            unsafe_allow_html=True)

        st.markdown(
            '''<style>
	    .black-link {
		color: black !important; /* 글씨 색상을 검정색으로 설정 */
		text-decoration: none; /* 밑줄 제거 */
	    }
	    .black-link:hover {
		text-decoration: underline; /* 마우스 호버 시 밑줄 표시 */
	    }
            </style>''', 
            unsafe_allow_html=True)

    with cols[-1]:
        login_button()

    button_css()

def button_css():
    st.markdown(
        """<style>
        div[data-testid="stMarkdownContainer"] p {
            font-size: 14px;/* !important;*/
        }
            </style>""",
        unsafe_allow_html=True,
    )

    # border
#        button[kind="secondary"] {
#            border: none !important;
#              }
