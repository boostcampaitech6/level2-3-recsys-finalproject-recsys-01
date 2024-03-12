import time, math

import streamlit as st
import pandas as pd
import numpy as np

import requests

from utils import page_header, get_response, patch_feedback 

def show_feedback_button(recipe_id, user_feedback):

    icon_mapper = lambda cooked: '❤️' if cooked else '🩶'
    cooked = recipe_id in user_feedback

    st.button(
        icon_mapper(cooked), 
        on_click=patch_feedback, 
        key=f'{recipe_id}_feedback_button', 
        args=(st.session_state.user, recipe_id, cooked))

def display_recipes_in_rows_of_four(recipe_list, user_feedback=None):

    for row in range(math.ceil(len(recipe_list)/4)):
        cols = st.columns(4)

        for i in range(4):
            item_idx = i + row * 4
            if item_idx >= len(recipe_list): break

            item = recipe_list[item_idx]
            with cols[i]:
                st.markdown(f'<a href="{item["recipe_img_url"]}" target="_blank"><img src="{item["recipe_img_url"]}" alt="Your Image" width=150 height=150/></a>', unsafe_allow_html=True)

                if user_feedback is None:
                    st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                else:
                    sub_cols = st.columns([3,1])
                    with sub_cols[0]:
                        st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                    with sub_cols[-1]:
                        show_feedback_button(item['recipe_id'], user_feedback)


def get_and_stack_recipe_data():
    
    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes/recommended?page={page_num}"
    recipe_list, user_feedback = [], []
    formatted_url = url.format(user_id=st.session_state.user, page_num=1)

    while formatted_url:
        print(formatted_url)
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']
        print(data['user_feedback'])
        user_feedback = data['user_feedback']

    return recipe_list, user_feedback

def recommendation_history_page():

    # 앱 헤더 
    page_header()

    # get data
    recipe_list, user_feedback = get_and_stack_recipe_data()

#    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes/recommended?page={page_num}"
#    user_id, page_num = 1,1
#    formatted_url = url.format(user_id=user_id, page_num=page_num)
#    data = get_response(formatted_url)

    # 페이지 구성
    container = st.container(border=True)

    with container:

        st.markdown("<h4 style='text-align: center;'>AI 가 선정한 취향 저격 레시피</h4>", unsafe_allow_html=True)
        
        sub_container = st.container(border=False)
        with sub_container:
            st.markdown("<div style='text-align: right; font-size: 12px;'>    ❤️: 요리해봤어요</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: right; font-size: 12px;'>🩶: 아직 안해봤어요</div>", unsafe_allow_html=True)

        display_ingredients_in_rows_of_four(recipe_list, user_feedback)

st.session_state['page_info'] = 'recommend_history'
recommendation_history_page()
