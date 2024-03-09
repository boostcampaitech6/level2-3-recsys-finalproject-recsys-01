import streamlit as st
import pandas as pd
import numpy as np
import time

from utils import menu_tab

user = '주디'

# page labeling
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# 상단바
menu_tab(login=True, user='Judy')

# 페이지 구성
container = st.container(border=True)

with container:
    st.markdown("<h4 style='text-align: center;'>이번 주 장바구니 만들기</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>예산을 정해주세요.</div>", unsafe_allow_html=True)

    cols = st.columns([1,5,1])
    with cols[1]:
        price = st.slider(
            label='', 
            min_value=10000,
            max_value=1000000, 
            value=50000,
            step=5000
        )

    cols = st.columns(5)
    with cols[2]:
        st.write("예산: ", price, '원')


    with cols[1]:
        button1 = st.button("이전 장바구니 보기")

    with cols[3]:
        button2 = st.button("다음 장바구니 보기", type="primary")

    st.markdown(
        """<style>
            div.stButton button {
            width: 150px;
        } 
        div[data-testid="stMarkdownContainer"] p {
            font-size: 16px;/* !important;*/
        }
            </style>""",
        unsafe_allow_html=True,
    )
