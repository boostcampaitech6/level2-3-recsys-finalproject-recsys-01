import streamlit as st
import requests

def set_result_page_2():
    st.session_state['page_info'] = 'result_page_2'

def post_recommendation():
    full_url = st.session_state.url_prefix + '/api/users/{user_id}/recommendations?price={price}'
    formatted_url = full_url.format(user_id=st.session_state.token['user_id'], price=st.session_state.price)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.session_state.token["token"]}',
    }

    data = requests.post(formatted_url, headers=headers)
    st.session_state.recommendation_result = data.json()
    st.session_state['page_info'] = 'result_page_1'

def recommendation_page():

    # 페이지 구성
    container = st.container(border=True)

    with container:
        st.markdown("<h4 style='text-align: center;'>이번 주 장바구니 만들기</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>AI 를 이용하여 당신의 입맛에 맞는 레시피와 필요한 식재료를 추천해줍니다.</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>예산을 정해주세요.</div>", unsafe_allow_html=True)

        cols = st.columns([1,5,1])

        if 'price' not in st.session_state:
            st.session_state.price = 50000

        def handle_change():
               st.session_state.price = st.session_state.price_slider

        with cols[1]:

            st.slider(
                label='price', min_value=10000, max_value=200000, value=50000, step=5000,
                on_change=handle_change, key='price_slider'
            )

        cols = st.columns(5)

        with cols[2]:
            st.write("예산: ", st.session_state.price, '원')

        if 'recommendation_result' in st.session_state:
            cols = st.columns([3,2,3,3])
            with cols[1]:
                button1 = st.button("이전 추천보기", on_click=set_result_page_2)
            with cols[2]:
                button2 = st.button("장바구니 추천받기", type="primary", on_click=post_recommendation)
        else:
            cols = st.columns([2,1.5,2])
            with cols[1]:
                button2 = st.button("장바구니 추천받기", type="primary", on_click=post_recommendation)
