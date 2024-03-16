import streamlit as st
import requests

def recommendation_page():

    # 페이지 구성
    container = st.container(border=True)

    with container:
        st.markdown("<h4 style='text-align: center;'>이번 주 장바구니 만들기</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>예산을 정해주세요.</div>", unsafe_allow_html=True)

        cols = st.columns([1,5,1])

        if 'price' not in st.session_state:
            st.session_state.price = 10000

        def handle_change():
               st.session_state.price = st.session_state.price_slider

        with cols[1]:

            st.slider(
                label='price', min_value=10000, max_value=1000000, value=50000, step=5000,
                on_change=handle_change, key='price_slider'
            )

        cols = st.columns(5)

        with cols[2]:
            st.write("예산: ", st.session_state.price, '원')


        cols = st.columns(3)

        with cols[1]:
            button2 = st.button("장바구니 추천받기", type="primary")
            if button2:
                st.session_state['page_info'] = 'result_page_1'
