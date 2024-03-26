import random, string
import streamlit as st
import streamlit_antd_components as sac

random_chars = lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=5))
APP_SERVER_PUBLIC_IP = "175.45.194.96"
APP_SERVER_PRIVATE_IP = "localhost" # "10.0.7.7"

def init():
    st.session_state.is_authenticated = False 
    st.session_state.page_info = "home"
    st.session_state.url_prefix = f"http://{APP_SERVER_PRIVATE_IP}:8000"
    st.session_state.url_main = f"http://{APP_SERVER_PUBLIC_IP}:8501/"

def set_logout_page():
    st.session_state.is_authenticated = False 
    st.session_state.page_info = "home"
    del st.session_state["password_correct"]

def set_login_page():
    st.session_state.page_info = 'login'

def set_signup_page():
    st.session_state.page_info = 'signup'

def login_button():
    cols = st.columns(2)
    if st.session_state.is_authenticated:
        with cols[0]:
            st.markdown(f"<p style='text-align: center;'>{st.session_state.token['user_id']}</p>", unsafe_allow_html=True)
            # st.write(f"{st.session_state.token['user_id']}님")
        with cols[1]:
            st.button(f"로그아웃", on_click=set_logout_page, key=f'logout_{st.session_state.page_info}_{random_chars()}')
    else:
        with cols[0]:
            st.button(f"회원가입", on_click=set_signup_page, key=f'signup_{st.session_state.page_info}_{random_chars()}')
        with cols[1]:
            st.button(f"로그인", on_click=set_login_page, key=f'login_{st.session_state.page_info}_{random_chars()}', type='primary')
    return login_button

def page_header():
    cols = st.columns([4, 1, 1, 1])
    
    # 나만의 장바구니
    with cols[0]:
        st.markdown(
            f'<h2><a href="{st.session_state.url_main}" target="_self" class="black-link">나만의 장바구니 🛒</a></h2>', 
            unsafe_allow_html=True)

    # log in button
    if st.session_state.is_authenticated:
        with cols[1]:
            st.markdown(f"<p style='text-align: center;font-size:20px'>{st.session_state.token['user_id']}님</p>", unsafe_allow_html=True)
        with cols[2]:
            st.button(f"로그아웃", on_click=set_logout_page, key=f'logout_{st.session_state.page_info}_{random_chars()}')
    button_css()
    link_css()
    display_css()
    
def link_css():
    st.markdown(
        '''<style>
	    .black-link {
		color: black !important; /* 글씨 색상을 검정색으로 설정 */
		text-decoration: none; /* 밑줄 제거 */
	    }
	    .black-link:hover {
		text-decoration: underline; /* 마우스 호버 시 밑줄 표시 */
	    }
        </style>
        ''', 
            unsafe_allow_html=True)

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

def display_css():
    
    st.markdown(
        '''
        <style>
        .food-label-home{
        margin:0 2 0 0;
        display: block;
        width: 100px;
        font-weight: bolder !important;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: normal;
        line-height: 1.2;
        text-align: left;
        word-wrap: break-word;
        display: -webkit-box;
        -webkit-line-clamp: 2 ;
        -webkit-box-orient: vertical;
        font-size: 12px !important;
        }
        
        .food-label{
        margin:2px;
        display: block;
        width: 120px;
        height: 28px;
        font-weight: bolder !important;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: normal;
        line-height: 1.2;
        text-align: left;
        word-wrap: break-word;
        display: -webkit-box;
        -webkit-line-clamp: 2 ;
        -webkit-box-orient: vertical;
        color: green;
        font-size: 12px !important;
        ''',
        unsafe_allow_html = True
        
    )