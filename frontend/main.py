import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from common import set_login_page, set_signup_page

def main_page():
    container3_1 = stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                    }
                    """,)
    with container3_1:
        st.markdown("<h4 style='text-align: center;'>나만의 식량 바구니에 \n 오신 것을 환영합니다!</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>자신의 입맞에 맞는 레시피를 저장하고 \n 이번주에 구매할 식량 바구니를 추천받아보세요</p>", unsafe_allow_html=True)
        
        cols = st.columns([4,2,2,3])
        with cols[1]:
            st.button(f"회원가입", on_click=set_signup_page, key=f'signup_{st.session_state.page_info}')
        with cols[2]:
            st.button(f"로그인", on_click=set_login_page, key=f'login_{st.session_state.page_info}', type='primary')

    container3_2 = st.container(border = True)

    with container3_2:
        st.markdown("<h4 style='text-align: center;'>사용 방법</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>회원 가입을 했을 때 어떤 기능을 쓸 수 있는지 살펴보는 페이지</p>", unsafe_allow_html=True)
        left_co, cent_co,last_co = st.columns((1, 8, 1))
        with cent_co:
            st.image('img/howto.png')
