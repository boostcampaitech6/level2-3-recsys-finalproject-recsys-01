import streamlit as st
from st_login_form import login_form
from streamlit_login_auth_ui.widgets import __login__
import math
import requests


global api_prefix
api_prefix = "http://localhost:8000/"

def set_logout():
    st.session_state.user = None
    st.session_state.is_authenticated = False 

def set_login():
    st.session_state.user = 'judy123' 
    st.session_state.is_authenticated = True

def login_button():
    if st.session_state.is_authenticated:
        login_button = st.button(f"{st.session_state.user}님 | 로그아웃", on_click=set_logout)
    else:
        login_button = st.button(f"회원가입 | 로그인", on_click=set_login)

    return login_button

def page_header():
    cols = st.columns([8,3])
    with cols[0]:
        st.header('나만의 식량 바구니')
    with cols[-1]:
        login_button()
    button_css()

def basket_feedback():
    st.markdown("<div style='text-align: center; font-size: 16px;'>방금 추천받은 장바구니 어땠나요?</div>", unsafe_allow_html=True)
    st.text("")
    cols = st.columns([3,1,1,3])
    with cols[1]:
        st.button('좋아요')
    with cols[2]:
        st.button('싫어요')

def get_response(formatted_url):
    response = requests.get(formatted_url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f'status code: {response.status_code}')
        data = None
    return data

def patch_feedback(user_id, recipe_id, current_state):
    url = api_prefix + "api/users/{user_id}/recipes/{recipe_id}/feedback"
    data = {
        'feedback': not current_state
        }
    response = requests.patch(url.format(user_id=user_id, recipe_id=recipe_id), json=data)
    print(f'status code: {response.status_code}')
    st.rerun()

def button_css():
    st.markdown(
        """<style>
        button[kind="secondary"] {
            border: none !important;
              }
        div[data-testid="stMarkdownContainer"] p {
            font-size: 14px;/* !important;*/
        }
            </style>""",
        unsafe_allow_html=True,
    )


def display_ingredients_in_rows_of_four2(ingredients):
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

def get_and_stack_recipe_data_w_feedback():
    
    url = api_prefix + "api/users/{user_id}/recipes/recommended?page={page_num}"
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
def display_recipes_in_rows_of_four(recipes):
    for recipe in recipes:
        sub_container = st.container(border=True)

        with sub_container:
            
            cols = st.columns(2)

            with cols[0]:
                st.markdown(f'<a href="{recipe["recipe_img_url"]}" target="_blank"><img src="{recipe["recipe_img_url"]}" alt="Your Image" width=100 height=100/></a>', unsafe_allow_html=True)

            with cols[1]:
                st.write(recipe['recipe_name'])
      
      

def get_and_stack_recipe_data():
    
    url = api_prefix + "api/users/{user_id}/recipes/cooked?page={page_num}"
    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.user, page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list

def get_my_recipe_data():
    
    url = api_prefix + "api/users/{user_id}/recipes/recommended?page={page_num}"
    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.user, page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list
