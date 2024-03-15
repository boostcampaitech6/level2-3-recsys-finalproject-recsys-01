import time, math

import pandas as pd
import numpy as np

import streamlit as st
import requests

from utils import page_header, get_response, patch_feedback 
from pages.RecommendationHistoryPage import display_ingredients_in_rows_of_four 

def get_and_stack_recipe_data():
    
    url = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/users/{user_id}/recipes/cooked?page={page_num}"
    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.user, page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list

def user_history_page():

    # 앱 헤더 
    page_header()

    # get data
    recipe_list = get_and_stack_recipe_data()

    # show container
    container = st.container(border=True)

    with container:
        # title
        st.markdown("<h4 style='text-align: center;'>❤️ 내가 요리한 레시피 ❤️</h4>", unsafe_allow_html=True)
        display_ingredients_in_rows_of_four(recipe_list)
        
# show UserHistoryPage
st.session_state['page_info'] = 'user_history'
user_history_page()
