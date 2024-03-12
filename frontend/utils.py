import streamlit as st
import requests

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

def basket_feedback():
    st.markdown("<div style='text-align: center; font-size: 16px;'>방금 추천받은 장바구니 어땠나요?</div>", unsafe_allow_html=True)
    st.text("")
    cols = st.columns([3,1,1,3])
    with cols[1]:
        st.button('좋아요')
    with cols[2]:
        st.button('싫어요')

def get_response(formatted_url):
    response = requests.get(formatted_url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f'status code: {response.status_code}')
        data = None
    return data

def patch_feedback(user_id, recipe_id, current_state):
    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes/{recipe_id}/feedback"
    data = {
        'feedback': not current_state
        }
    response = requests.patch(url.format(user_id=user_id, recipe_id=recipe_id), json=data)
    print(f'status code: {response.status_code}')
    st.rerun()

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

#        button[kind="primary"] {
#          }
#          button[kind="seondary"] {
#            div.stButton button {
#            width: 150px;
#            border: none !important;
#        } 
