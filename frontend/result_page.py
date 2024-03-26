import math

import streamlit as st
import requests
from common import display_css, link_css
from user_history import display_recipes_in_rows_of_four


def set_recommendation():
    st.session_state['page_info'] = 'recommendation'

def display_ingredients_in_rows_of_four(ingredients):
    for ingredient in ingredients:
        sub_container = st.container(border=True)

        with sub_container:
            
            cols = st.columns([2, 4, 1])

            with cols[0]:
                st.markdown(f'<a href="{ingredient["market_url"]}" target="_blank"><img src="{ingredient["img_link"]}" alt="Your Image" width=100 height=100/></a>', unsafe_allow_html=True)

            with cols[1]:
                st.write(ingredient['ingredient_name'], ingredient['ingredient_amount'], ingredient['ingredient_unit'])
                st.write(round(ingredient['ingredient_price']), '원')
            
            with cols[-1]:
                st.link_button('구매', ingredient['market_url'], type='primary')


def basket_feedback():
    st.markdown("<div style='text-align: center; font-size: 16px;'>방금 추천받은 장바구니 어땠나요?</div>", unsafe_allow_html=True)
    st.text("")
    cols = st.columns([2,1,1,2])
    with cols[1]:
        st.button('좋아요')
    with cols[2]:
        st.button('싫어요')

def post_recommendation():
    full_url = st.session_state.url_prefix + '/api/users/{user_id}/recommendations?price={price}'
    formatted_url = full_url.format(user_id=st.session_state.token['user_id'], price=st.session_state.price)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.session_state.token["token"]}',
    }

    data = requests.post(formatted_url, headers=headers)
    return data.json()
#    response_json = response.json() if response.status_code == 200 else None
#
#    return response.status_code, response_json

def result_page():

#    # 앱 헤더 
#    page_header()

#    url = api_prefix + "users/{user_id}/previousrecommendation"
#    formatted_url = url.format(user_id=st.session_state.user)
#    data = get_response(formatted_url)
    #data = post_recommendation()
    data = st.session_state.recommendation_result

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

        st.markdown(f"<h5 style='text-align: center;'>예상 총 금액: {round(total_price)} 원</h5>", unsafe_allow_html=True)
        
        st.divider()

        # 이 장바구니로 만들 수 있는 음식 레시피
        st.markdown("<h4 style='text-align: center;'>이 장바구니로 만들 수 있는 음식 레시피</h4>", unsafe_allow_html=True)
        display_recipes_in_rows_of_four(data['recipe_list'])

        st.text("\n\n")

        st.divider()
        st.markdown("<h4 style='text-align: center;'>다른 예산으로도 추천받아 볼까요?</h4>", unsafe_allow_html=True)
        cols = st.columns([2, 3, 1])
        with cols[1]:
            button2 = st.button("추천받으러 가기 >>", type="primary", on_click=set_recommendation)
        
        display_css()
        link_css()
