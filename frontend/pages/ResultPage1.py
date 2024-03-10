import streamlit as st
import pandas as pd
import numpy as np
import time

from utils import menu_tab, basket_feedback

user = '주디'
ingredients = [
        {'ingredient_name': '브로콜리', 
         'amount': 1, 'unit': 'kg', 
         'price': 4680,
         'img_url': 'https://health.chosun.com/site/data/img_dir/2024/01/19/2024011902009_0.jpg', 
         'market_url': 'https://www.coupang.com/vp/products/4874444452?itemId=6339533080&vendorItemId=73634892616&pickType=COU_PICK&q=%EB%B8%8C%EB%A1%9C%EC%BD%9C%EB%A6%AC&itemsCount=36&searchId=891d0b69dc8f452daf392e3db2482732&rank=1&isAddedCart='},
        {'ingredient_name': '초고추장', 
         'amount': 500, 'unit': 'g', 
         'price': 5000,
         'img_url': 'https://image7.coupangcdn.com/image/retail/images/4810991441045098-31358d86-eff6-45f4-8ed6-f36b642e8944.jpg', 
         'market_url': 'https://www.coupang.com/vp/products/6974484284?itemId=17019959259&vendorItemId=3000138402&q=%EC%B4%88%EA%B3%A0%EC%B6%94%EC%9E%A5&itemsCount=36&searchId=d5538b6e86d04be3938c98ef1655df85&rank=1&isAddedCart='},
        ]

# page labeling
st.set_page_config(
    page_title="ResultPage-1",
)

# 상단바
menu_tab(login=True, user='Judy')

# 페이지 구성
container = st.container(border=True)

with container:

    st.markdown("<h4 style='text-align: center;'>새로운 장바구니를 추천받았어요!</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 16px;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<h4 style='text-align: left;'>추천 장바구니</h4>", unsafe_allow_html=True)

    total_price = 0

    for ingredient in ingredients:
        sub_container = st.container(border=True)

        with sub_container:
            
            cols = st.columns(5)
            with cols[0]:
                st.image(ingredient['img_url'])
            with cols[1]:
                st.write(ingredient['ingredient_name'])
                st.write(ingredient['amount'], ingredient['unit'])
            
            with cols[-1]:
                st.link_button('구매', ingredient['market_url'], type='primary')

        total_price += ingredient['price']

    st.markdown(f"<h5 style='text-align: center;'>예상 총 금액: {total_price} 원</h5>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<h4 style='text-align: center;'>이 장바구니로 만들 수 있는 음식 레시피</h4>", unsafe_allow_html=True)

    foods = [
        '어묵김말이',
        '두부새우전',
        '알밥',
        '현미호두죽',
    ]

    img_urls = [
        'https://recipe1.ezmember.co.kr/cache/recipe/2015/05/18/1fb83f8578488ba482ad400e3b62df49.jpg',
        'https://recipe1.ezmember.co.kr/cache/recipe/2015/06/09/8d7a003794ac7ab77e5777796d9c20dd.jpg',
        'https://recipe1.ezmember.co.kr/cache/recipe/2015/06/09/54d80fba5f2615d0a6bbd960adf4296c.jpg',
        'https://recipe1.ezmember.co.kr/cache/recipe/2017/07/19/993a1efe45598cf296076874df509bfe1.jpg',
    ]

    recipe_urls = [
        'https://www.10000recipe.com/recipe/128671',
        'https://www.10000recipe.com/recipe/128892',
        'https://www.10000recipe.com/recipe/128932',
        'https://www.10000recipe.com/recipe/131871',
    ]

    feedback = [ True, False, False, True ]
    
    for url in range(int(len(img_urls)/4)):
        cols = st.columns(4)

        for i in range(4):
            with cols[i]:
                st.markdown(f'<a href="{recipe_urls[i]}" target="_blank"><img src="{img_urls[i]}" alt="Your Image" width=150 height=150/></a>', unsafe_allow_html=True)
                
                sub_cols = st.columns([3,1])
                with sub_cols[0]:
                    st.markdown(f'<p class="food-label">{foods[i]}</p>', unsafe_allow_html=True)

                if feedback[i]:
                    btn_label = '❤️'
                else:
                    btn_label = '🩶'
                with sub_cols[-1]:
                    st.markdown(f'<button class="button0">{btn_label}</button>', unsafe_allow_html=True)
                    # POST /api/users/{user_id}/foods
                    # inputs: user_id, List[food_id]

    st.text("\n\n")

    basket_feedback()


st.markdown("""
    <style>
    .food-label {
        font-size:14px !important;
        }
    .button0 {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        font-size: 18px;
        font-weight: bolder;
        cursor: pointer;
        border: none !important;
        vertical-align: middle;
    </style>
    """, unsafe_allow_html=True)
