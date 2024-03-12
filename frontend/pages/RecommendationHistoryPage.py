import streamlit as st
import pandas as pd
import numpy as np
import time

import requests

from utils import page_header, get_response, patch_feedback 

user = '주디'
user_id = '1'
page_num = '1'

def recommendation_history_page():

    # 앱 헤더 
    page_header(False, None)

    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes/recommended?page={page_num}"
    user_id, page_num = 1,1
    formatted_url = url.format(user_id=user_id, page_num=page_num)
    data = get_response(formatted_url)

    # 페이지 구성
    container = st.container(border=True)

    with container:

        st.markdown("<h4 style='text-align: center;'>AI 가 선정한 취향 저격 레시피</h4>", unsafe_allow_html=True)
        
        sub_container = st.container(border=False)
        with sub_container:
            st.markdown("<div style='text-align: right; font-size: 12px;'>    ❤️: 요리해봤어요</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: right; font-size: 12px;'>🩶: 아직 안해봤어요</div>", unsafe_allow_html=True)

        recipe_list = data['recipe_list']
        for row in range(int(len(recipe_list)/4)):
            cols = st.columns(4)

            for i in range(4):
                if row == len(recipe_list)//4: i = len(recipe_list)%4

                with cols[i]:
                    st.markdown(f'<a href="{recipe_list[i]["recipe_img_url"]}" target="_blank"><img src="{recipe_list[i]["recipe_img_url"]}" alt="Your Image" width=150 height=150/></a>', unsafe_allow_html=True)
                    
                    sub_cols = st.columns([3,1])
                    with sub_cols[0]:
                        st.markdown(f'<p class="food-label">{recipe_list[i]["recipe_name"]}</p>', unsafe_allow_html=True)

                    icon_mapper = lambda cooked: '❤️' if cooked else '🩶'
                    cooked = recipe_list[i]['recipe_id'] in data['user_feedback']

                    with sub_cols[-1]:
                        st.button(
                            icon_mapper(cooked), 
                            on_click=patch_feedback, 
                            key=f'feedback_{i}', 
                            args=(user_id, recipe_list[i]['recipe_id'], cooked))

st.session_state['page_info'] = 'recommend_history'
recommendation_history_page()
