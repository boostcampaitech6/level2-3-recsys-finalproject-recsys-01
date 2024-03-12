import time, math

import pandas as pd
import numpy as np

from PIL import Image
import streamlit as st
import requests

from utils import page_header, basket_feedback, get_response, patch_feedback 
from pages.RecommendationHistoryPage import display_ingredients_in_rows_of_four

def display_ingredients_in_rows_of_four(ingredients):
    for ingredient in ingredients:
        sub_container = st.container(border=True)

        with sub_container:
            
            cols = st.columns(5)

            with cols[0]:
                st.markdown(f'<a href="{ingredient["img_link"]}" target="_blank"><img src="{ingredient["img_link"]}" alt="Your Image" width=100 height=100/></a>', unsafe_allow_html=True)

            with cols[1]:
                st.write(ingredient['ingredient_name'])
                st.write(ingredient['ingredient_amount'], ingredient['ingredient_unit'])
            
            with cols[-1]:
                st.link_button('구매', ingredient['market_url'], type='primary')

def result_page_2():

    # 앱 헤더 
    page_header()

    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/previousrecommendation"
    formatted_url = url.format(user_id=st.session_state.user)
    data = get_response(formatted_url)

    # 페이지 구성
    container = st.container(border=True)

    with container:

        # 장바구니 추천 문구
        st.markdown("<h4 style='text-align: center;'>새로운 장바구니를 추천받았어요!</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 16px;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)

        st.divider()

        # 구매할 식료품 목록
        st.markdown("<h4 style='text-align: left;'>추천 장바구니</h4>", unsafe_allow_html=True)

        display_ingredients_in_rows_of_four(data['ingredient_list'])
        total_price = sum([ingredient['ingredient_price'] for ingredient in data['ingredient_list']])

        st.markdown(f"<h5 style='text-align: center;'>예상 총 금액: {total_price} 원</h5>", unsafe_allow_html=True)
        
        st.divider()

        # 이 장바구니로 만들 수 있는 음식 레시피
        st.markdown("<h4 style='text-align: center;'>이 장바구니로 만들 수 있는 음식 레시피</h4>", unsafe_allow_html=True)
        display_ingredients_in_rows_of_four(data['recipe_list'])

        st.text("\n\n")
        basket_feedback()

st.session_state['page_info'] = "result_page_2" 
result_page_2()
