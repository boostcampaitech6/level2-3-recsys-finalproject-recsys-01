import streamlit as st

from main_2 import get_response
from user_history import display_recipes_in_rows_of_four

def get_and_stack_recipe_data_w_feedback():
    
    url = st.session_state.url_prefix + "/api/users/{user_id}/recipes/recommended?page={page_num}"
    recipe_list, user_feedback = [], []
    formatted_url = url.format(user_id=st.session_state.token['user_id'], page_num=1)

    while formatted_url:
        #print(formatted_url)
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']
        #print(data['cooked_recipes_id'])
        user_feedback = data['cooked_recipes_id']
    
    return recipe_list, user_feedback

def recommendation_history_page():

    # get data
    recipe_list, user_feedback = get_and_stack_recipe_data_w_feedback()

    # 페이지 구성
    container = st.container(border=True)

    with container:

        st.markdown("<h4 style='text-align: center;'>AI가 선정한 취향저격 레시피 🤖</h4>", unsafe_allow_html=True)
        
        sub_container = st.container(border=False)
        with sub_container:
            st.markdown("<div style='text-align: right; font-size: 12px;'>    ❤️: 요리해봤어요</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: right; font-size: 12px;'>🤍: 아직 안해봤어요</div>", unsafe_allow_html=True)

        display_recipes_in_rows_of_four(recipe_list, user_feedback)
