import streamlit as st
import requests

from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page


def get_response(formatted_url):
    response = requests.get(formatted_url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f'status code: {response.status_code}')
        data = None
    return data

def get_my_recipe_data():
    
    url = st.session_state.url_prefix + "/api/users/{user_id}/recipes/cooked?page_num={page_num}"

    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.token['user_id'], page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list

def get_my_recommended_data():
    
    url = st.session_state.url_prefix + "/api/users/{user_id}/recipes/recommended?page_num={page_num}"

    recipe_list = []
    formatted_url = url.format(user_id=st.session_state.token['user_id'], page_num=1)

    while formatted_url:
        data = get_response(formatted_url)
        recipe_list.extend(data['recipe_list'])
        formatted_url = data['next_page_url']

    return recipe_list

def display_my_recipe_container(my_recipe_list): 

    container3_4 = st.container(border = True)
    with container3_4:
        cols = st.columns([6,1])
        with cols[0]:
            st.markdown("<h4 style='text-align: left;'>내가 요리한 레시피</h4>", unsafe_allow_html=True)
        with cols[1]:
            if st.button("더보기", key='more_user_history'):
                switch_page("user_history")

        cols = st.columns((1, 1, 1, 1, 1))
        
        for i, my_recipe in enumerate(my_recipe_list[:5]):
            with cols[i]:
                with st.container(border=True):
                    # st.image(my_recipe["recipe_img_url"])
                    st.markdown(f'<a href="{my_recipe["recipe_url"]}" target="_blank"><img src="{my_recipe["recipe_img_url"]}" alt="Your Image" width=90 height=90/></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>{my_recipe['recipe_name']}</p>", unsafe_allow_html=True)

def display_recommended_container(recommended_list): 

    container3_4 = st.container(border = True)

    with container3_4:
        cols = st.columns([6,1])
        with cols[0]:
            st.markdown("<h4 style='text-align: left;'>내가 좋아할 레시피</h4>", unsafe_allow_html=True)
        with cols[1]:
            if st.button("더보기", key='more_recommendation_history'):
                switch_page("recommendation_history")
            
        cols = st.columns((1, 1, 1, 1, 1))
        
        for i, recommended in enumerate(recommended_list[:5]):
            with cols[i]:
                with st.container(border=True):
                    # st.image(recommended["recipe_img_url"])
                    st.markdown(f'<a href="{recommended["recipe_url"]}" target="_blank"><img src="{recommended["recipe_img_url"]}" alt="Your Image" width=90 height=90/></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>{recommended['recipe_name']}</p>", unsafe_allow_html=True)

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
    
    # recommended_preview 
    recommended_list = get_my_recommended_data()
    display_recommended_container(recommended_list)

    # user_history_preview
    my_recipe_list = get_my_recipe_data()
    display_my_recipe_container(my_recipe_list)
