import streamlit as st
import pandas as pd
import numpy as np
import time

from utils import menu_tab
import requests

user = '주디'
user_id = '1'
page_num = '1'

# page labeling
st.set_page_config(
    page_title="RecommendationHistoryPage",
)

# 상단바
menu_tab(login=True, user='Judy')

# RecommendationHistoryByPage request
response = requests.get(f"https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes?page={page_num}")
if response.status_code == 200:
    data = response.json()['food_list']
else:
    print(f'status code: {response.status_code}')
    data = None

# 페이지 구성
container = st.container(border=True)

with container:

    st.markdown("<h4 style='text-align: center;'>AI 가 선정한 취향 저격 레시피</h4>", unsafe_allow_html=True)
    
    sub_container = st.container(border=False)

    with sub_container:
        st.markdown("<div style='text-align: right; font-size: 12px;'>    ❤️: 요리해봤어요</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: right; font-size: 12px;'>🩶: 아직 안해봤어요</div>", unsafe_allow_html=True)


#    foods = [
#        '어묵김말이',
#        '두부새우전',
#        '알밥',
#        '현미호두죽',
#    ]
#
#    img_urls = [
#        'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/18/1fb83f8578488ba482ad400e3b62df49.jpg',
#        'https://recipe1.ezmember.co.kr/cache/recipe/2015/06/09/8d7a003794ac7ab77e5777796d9c20dd.jpg',
#        'https://recipe1.ezmember.co.kr/cache/recipe/2015/06/09/54d80fba5f2615d0a6bbd960adf4296c.jpg',
#        'https://recipe1.ezmember.co.kr/cache/recipe/2017/07/19/993a1efe45598cf296076874df509bfe1.jpg',
#    ]
#
#    recipe_urls = [
#        'https://www.10000recipe.com/recipe/128671',
#        'https://www.10000recipe.com/recipe/128892',
#        'https://www.10000recipe.com/recipe/128932',
#        'https://www.10000recipe.com/recipe/131871',
#    ]

    feedback = [ True, False, False, True ]
    
    #for url in range(int(len(img_urls)/4)):
    for row in range(int(len(data)/4)):
        cols = st.columns(4)

        for i in range(4):
            if row == len(data)//4: i = len(data)%4
            with cols[i]:
                st.markdown(f'<a href="{data[i]["food_img_url"]}" target="_blank"><img src="{data[i]["food_img_url"]}" alt="Your Image" width=150 height=150/></a>', unsafe_allow_html=True)
                
                sub_cols = st.columns([3,1])
                with sub_cols[0]:
                    st.markdown(f'<p class="food-label">{data[i]["food_name"]}</p>', unsafe_allow_html=True)

                if feedback[i]:
                    btn_label = '❤️'
                else:
                    btn_label = '🩶'
                with sub_cols[-1]:
                    st.markdown(f'<button class="button0">{btn_label}</button>', unsafe_allow_html=True)
                    # POST /api/users/{user_id}/foods
                    # inputs: user_id, List[food_id]


st.markdown("""
    <style>
    .food-label {
        font-size:14px !important;
        }
    .button0 {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        font-size: 18px;
        font-weight: bolder;
        cursor: pointer;
        border: none !important;
        vertical-align: middle;
    </style>
    """, unsafe_allow_html=True)
