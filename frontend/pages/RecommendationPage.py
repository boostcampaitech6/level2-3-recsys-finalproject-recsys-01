import streamlit as st
import pandas as pd
import numpy as np
import time

from utils import page_header, basket_feedback
from pages.ResultPage2 import result_page_2

def recommendation_page():

    # 앱 헤더 
    page_header(False, None)

    # 페이지 구성
    container = st.container(border=True)

    with container:
        st.markdown("<h4 style='text-align: center;'>이번 주 장바구니 만들기</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>예산을 정해주세요.</div>", unsafe_allow_html=True)

        cols = st.columns([1,5,1])

        with cols[1]:

            price = st.slider(
                label='', min_value=10000, max_value=1000000, value=50000, step=5000
            )

        cols = st.columns(5)

        with cols[2]:
            st.write("예산: ", price, '원')


        cols = st.columns(3)

        with cols[1]:
            button2 = st.button("장바구니 추천받기", type="primary")
            if button2:
                st.session_state['page_info'] = 'result_page_1'


# 이전 추천 목록 조회
if 'page_info' not in st.session_state:
    st.session_state['page_info'] = 'recommend'

if st.session_state['page_info'] == 'result_page_1':
    result_page_2()
else:
    recommendation_page()
