import math
import streamlit as st
import requests

from main_2 import get_response
from common import display_css

def get_and_stack_recipe_data():
    
    url = st.session_state.url_prefix + "/api/users/{user_id}/recipes/cooked?page={page_num}"
    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.token['user_id'], page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list

def display_recipes_in_rows_of_four(recipe_list, user_feedback=None):

    for row in range(math.ceil(len(recipe_list)/4)):
        cols = st.columns(4)

        for i in range(4):
            item_idx = i + row * 4
            if item_idx >= len(recipe_list): break

            item = recipe_list[item_idx]
            
            with cols[i]:
                # with st.container(border=True):
                #     st.markdown(f'<a href="{item["recipe_img_url"]}" target="_blank"><img src="{item["recipe_img_url"]}" alt="Your Image" width=120 height=120/></a>', unsafe_allow_html=True)

                #     if user_feedback is None:
                #         st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                #     else:
                #         sub_cols = st.columns([3,1])
                #         with sub_cols[0]:
                #             st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                #         with sub_cols[-1]:
                #             show_feedback_button(item['id'], user_feedback)
                #     display_css()
                with st.container(border=True):
                    st.markdown(f'<a href="{item["recipe_url"]}" target="_blank"><img src="{item["recipe_img_url"]}" alt="Your Image" width=120 height=120/></a>', unsafe_allow_html=True)

                    if user_feedback is None:
                        st.markdown(f'<a href="{item["recipe_url"]}" target="_blank" class="black-link"><p class="food-label">{item["recipe_name"]}</p></a>', unsafe_allow_html=True)
                        display_css()
                    else:
                        
                        st.markdown(f'<a href="{item["recipe_url"]}" target="_blank" class="black-link"><p class="food-label">{item["recipe_name"]}</p></a>', unsafe_allow_html=True)
                        sub_cols = st.columns([3,1, 1])
                        with sub_cols[-2]:
                            show_feedback_button(item['id'], user_feedback)

def patch_feedback(user_id, recipe_id, current_state):
    url = st.session_state.url_prefix + "/api/users/{user_id}/recipes/{recipe_id}/feedback"
    data = {
        'feedback': not current_state
        }
    response = requests.patch(url.format(user_id=st.session_state.token['user_id'], recipe_id=recipe_id), json=data)
    print(f'status code: {response.status_code}')

def show_feedback_button(recipe_id, user_feedback):

    icon_mapper = lambda cooked: '❤️' if cooked else '🤍'
    cooked = recipe_id in user_feedback

    st.button(
        icon_mapper(cooked), 
        on_click=patch_feedback, 
        key=f'{recipe_id}_feedback_button', 
        args=(st.session_state.token['user_id'], recipe_id, cooked))
    
def user_history_page():

    # get data
    recipe_list = get_and_stack_recipe_data()

    # show container
    container = st.container(border=True)

    with container:
        # title
        st.markdown("<h4 style='text-align: center;'>내가 요리한 레시피 🥘</h4>", unsafe_allow_html=True)
        display_recipes_in_rows_of_four(recipe_list)
