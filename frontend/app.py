import streamlit as st
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container
from st_supabase_connection import SupabaseConnection
from st_login_form import login_form
from streamlit_login_auth_ui.widgets import __login__
import time, math

import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image
import requests

global api_prefix
api_prefix = "https://3cc9be7f-84ef-480e-af0d-f4e81b375f2e.mock.pstmn.io/api/"

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
    
    url = api_prefix + "users/{user_id}/recipes/recommended?page={page_num}"
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

    # 페이지 구성
    container = st.container(border=True)

    with container:

        st.markdown("<h4 style='text-align: center;'>AI 가 선정한 취향 저격 레시피</h4>", unsafe_allow_html=True)
        
        sub_container = st.container(border=False)
        with sub_container:
            st.markdown("<div style='text-align: right; font-size: 12px;'>    ❤️: 요리해봤어요</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: right; font-size: 12px;'>🩶: 아직 안해봤어요</div>", unsafe_allow_html=True)

        display_ingredients_in_rows_of_four2(recipe_list, user_feedback)


def recommendation_page():

    # 앱 헤더 
    page_header()

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
            
                

def result_page_2():

    # 앱 헤더 
    page_header()

    url = api_prefix + "users/{user_id}/previousrecommendation"
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
        display_recipes_in_rows_of_four(data['recipe_list'])

        st.text("\n\n")
        basket_feedback()


def get_and_stack_recipe_data():
    
    url = api_prefix + "users/{user_id}/recipes/cooked?page={page_num}"
    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.user, page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list



def get_my_recipe_data():
    
    url = api_prefix + "users/{user_id}/recipes/recommended?page={page_num}"
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
        
# , signin_page, login_page, signin_page_2, signin_page_3, main_page_2
menu_titles = ["house", "🛒이번주 장바구니 추천", "😋내가 요리한 레시피", "🔎취향저격 레시피", "Log In / 회원가입"]

def main_page():
    container3_1 = stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                    }
                    """,)
    with container3_1:
        st.markdown("<h4 style='text-align: center;'>나만의 식량 바구니에 \n 오신 것을 환영합니다!</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>자신의 입맞에 맞는 레시피를 저장하고 \n 이번주에 구매할 식량 바구니를 추천받아보세요</p>", unsafe_allow_html=True)
        
        btn = sac.buttons(
            items=['로그인', '회원가입'],
            index=0,
            format_func='title',
            align='center',
            direction='horizontal',
            radius='lg',
            return_index=False
        )
        
    container3_2 = st.container(border = True)
    with container3_2:
        st.markdown("<h4 style='text-align: center;'>사용 방법</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>회원 가입을 했을 때 어떤 기능을 쓸 수 있는지 살펴보는 페이지</p>", unsafe_allow_html=True)
        left_co, cent_co,last_co = st.columns((1, 8, 1))
        with cent_co:
            st.image('img/howto.png')
    
def signin_page():
    container3 = st.container(border = True)
    with container3:
        st.markdown(f"<h4 style='text-align: center;'>{menu_titles[4]}</h4>", unsafe_allow_html=True)

        __login__obj = __login__(
            auth_token = "courier_auth_token", 
            company_name = "Shims",
            width = 200, height = 250, 
            logout_button_name = 'Logout',
            hide_menu_bool = False, 
            hide_footer_bool = False)

        LOGGED_IN = __login__obj.build_login_ui()

        if LOGGED_IN == True:
            st.markown("Your Streamlit Application Begins here!")
    
def user_history_page():
    
    recipe_list = get_and_stack_recipe_data()

    container = st.container(border=True)

    my_recipe_list = get_my_recipe_data()
    
    container3 = st.container(border=True)
    with container3:
        st.markdown("<h4 style='text-align: center;'>최근에 만들었던 음식을 골라주세요</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>5개 이상 선택해 주세요</p>", unsafe_allow_html=True)
        cols2 = st.columns([4,4])
        
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                my_recipe = my_recipe_list[0]
                st.image(my_recipe["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe['recipe_name']}</p>", unsafe_allow_html=True)
        with col2:
            with st.container(border=True):
                my_recipe = my_recipe_list[1]
                st.image(my_recipe["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe['recipe_name']}</p>", unsafe_allow_html=True)
        with col3:
            with st.container(border=True):
                my_recipe = my_recipe_list[2]
                st.image(my_recipe["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe['recipe_name']}</p>", unsafe_allow_html=True)
        with col4:
            with st.container(border=True):
                my_recipe = my_recipe_list[3]
                st.image(my_recipe["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe['recipe_name']}</p>", unsafe_allow_html=True)

        btn = sac.buttons(
            items=['더 보기', '다음 단계'],
            index=0,
            format_func='title',
            align='center',
            direction='horizontal',
            radius='lg',
            return_index=False,
        )

def main_page_2():
    container3_1 = stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        background-color: white;
                    }
                    """,)
    with container3_1:
        st.markdown("<h4 style='text-align: center;'>나만의 식량 바구니에 \n 오신 것을 환영합니다!</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>자신의 입맞에 맞는 레시피를 저장하고 \n 이번주에 구매할 식량 바구니를 추천받아보세요</p>", unsafe_allow_html=True)
    
    my_recipe_list = get_my_recipe_data()
    # 취향저격 레시피
    container3_4 = st.container(border = True)
    with container3_4:
        st.markdown("<h4 style='text-align: left;'>내가 해먹은 레시피  </h4>", unsafe_allow_html=True)
        
        col_1, col_2, col_3, col_4, col_5 = st.columns((1, 1, 1, 1, 1))
        
        with col_1:
            with st.container(border=True):
                st.image(my_recipe_list[0]["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe_list[0]['recipe_name']}</p>", unsafe_allow_html=True)
        with col_2:
            with st.container(border=True):
                st.image(my_recipe_list[1]["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe_list[1]['recipe_name']}</p>", unsafe_allow_html=True)
        with col_3:
            with st.container(border=True):
                st.image(my_recipe_list[2]["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe_list[2]['recipe_name']}</p>", unsafe_allow_html=True)
        with col_4:
            with st.container(border=True):
                #col_l, col_c, 
                st.image(my_recipe_list[3]["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe_list[3]['recipe_name']}</p>", unsafe_allow_html=True)
        with col_5:
            with st.container(border=True):
                st.image(my_recipe_list[4]["recipe_img_url"])
                st.markdown(f"<p style='text-align: center;'>{my_recipe_list[4]['recipe_name']}</p>", unsafe_allow_html=True)
    
    
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
    url = api_prefix + "users/{user_id}/recipes/{recipe_id}/feedback"
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


st.set_page_config(layout="wide")

# 세션 초기화
if 'page_info' not in st.session_state:
    st.session_state['page_info'] = 'home'

# 로그인되어 있다고 가정
def init():
    st.session_state.user = 1 
    st.session_state.is_authenticated = True

# 로그인 상태 초기화
init()


# page_info 설정
st.session_state['page_info'] = 'home'


app_title = "🛒 나만의 식량 바구니"
menu_titles = ["house", "🛒이번주 장바구니 추천", "😋내가 요리한 레시피", "🔎취향저격 레시피", "Log In / 회원가입", "MainPage-2", "User history"]
################

################
# body -> main -> sub
container1 = st.container(border=True)
with container1:
    cols = st.columns([1,2])
    with cols[0]:
        st.markdown(f"<h4> {app_title} </h4>", unsafe_allow_html=True)
    with cols[1]:
        seg = sac.segmented(
            items=[
                sac.SegmentedItem(icon=menu_titles[0]),
                sac.SegmentedItem(label=menu_titles[1]),
                sac.SegmentedItem(label=menu_titles[2]),
                sac.SegmentedItem(label=menu_titles[3]),
                sac.SegmentedItem(label=menu_titles[4]),
                sac.SegmentedItem(label=menu_titles[5]),
                sac.SegmentedItem(label=menu_titles[6]),
            ], align='center', use_container_width=True,
        )

    container2 = st.container(border=True)
    with container2:
        if seg == menu_titles[1]:
            # 🛒이번주 장바구니 추천
            container3 = st.container(border=True)
            with container3:
                st.markdown(f"<h4 style='text-align: center;'>{menu_titles[1]}</h4>", unsafe_allow_html=True)
            
                if 'page_info' not in st.session_state:
                    st.session_state['page_info'] = 'recommend'

                if st.session_state['page_info'] == 'result_page_1':
                    result_page_2()
                else:
                    recommendation_page()
                
        elif seg == menu_titles[2]:
            # 😋내가 요리한 레시피
            st.session_state['page_info'] = 'recommend_history'
            main_page_2()
        elif seg == menu_titles[3]:
            st.session_state['page_info'] = 'recommend_history'
            main_page_2()
        elif seg == menu_titles[4]:
            # 로그인 / 회원가입
            signin_page()
        elif seg == menu_titles[5]:
            # MainPage_2
            # main_page_2()
            
            st.session_state['page_info'] = "result_page_2" 
            result_page_2()
        elif seg == menu_titles[6]:
            
            # show UserHistoryPage
            st.session_state['page_info'] = 'user_history'
            user_history_page()
        else :
            # Home
            main_page()
            