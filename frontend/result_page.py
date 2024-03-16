import math

import streamlit as st
import requests

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

def display_recipes_in_rows_of_four(recipe_list, user_feedback=None):

    for row in range(math.ceil(len(recipe_list)/4)):
        cols = st.columns(4)

        for i in range(4):
            item_idx = i + row * 4
            if item_idx >= len(recipe_list): break

            item = recipe_list[item_idx]
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f'<a href="{item["recipe_url"]}" target="_blank"><img src="{item["recipe_img_url"]}" alt="Your Image" width=120 height=120/></a>', unsafe_allow_html=True)

                    if user_feedback is None:
                        st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                    else:
                        sub_cols = st.columns([3,1])
                        with sub_cols[0]:
                            st.markdown(f'<p class="food-label">{item["recipe_name"]}</p>', unsafe_allow_html=True)
                        with sub_cols[-1]:
                            show_feedback_button(item['recipe_id'], user_feedback)

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
    data = post_recommendation()

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
