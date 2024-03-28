import math
import streamlit as st
import requests

from main_2 import get_response

def inquire_all_recipes(page_url):
    data = get_response(page_url)
    return data['foods'], data['next_page_url']

def show_recipes(page_num):
    recipe_list, next_page_url = inquire_all_recipes(page_num)
    checkboxes = display_recipes_in_four_by_four(recipe_list)
    return checkboxes, next_page_url

def add_next_page_url(next_page_url):
    st.session_state['page_urls'].append(st.session_state.url_prefix + next_page_url)

def post_cooked_recipes(cooked_recipes, all_checkboxes):
    if sum(all_checkboxes.values()) < 5:
        st.session_state['page_warn'] = True
        return

    url = st.session_state.url_prefix + "/api/users/{user_id}/foods"

    data = {
        'recipes': cooked_recipes
        }

    headers = {
        'Content-Type': 'application/json'
    }

    formatted_url = url.format(user_id=st.session_state.token['user_id'])
    response = requests.post(formatted_url, headers=headers, json=data)
    st.session_state.token['is_first_login'] = False
    if response.status_code == '201':
        print('successfully updated')
    else:
        print(response.status_code)

def display_recipes_in_four_by_four(recipe_list):
    checkboxes = {}

    for row in range(math.ceil(len(recipe_list)/4)):

        cols = st.columns(4)

        for i in range(4):
            item_idx = i + row * 4
            if item_idx >= len(recipe_list): break

            item = recipe_list[item_idx]
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f'<a href="{item["recipe_img_url"]}" target="_blank"><img src="{item["recipe_img_url"]}" alt="Your Image" width=120 height=120/></a>', unsafe_allow_html=True)

                
                    sub_cols = st.columns([1, 5])
                    checkboxes[item['_id']] = st.checkbox(label=item["recipe_name"], key=f'checkbox_{item["_id"]}')

    return checkboxes 

def choose_food_page():

    # 첫 페이지만 page_urls에 추가
    if 'page_urls' not in st.session_state:
        url = st.session_state.url_prefix + "/api/users/foods?page_num={page_num}"
        page_url = url.format(page_num=1)
        st.session_state['page_urls'] = [page_url]

    if 'page_warn' not in st.session_state:
        st.session_state['page_warn'] = False

    # 체크박스 모니터링
    all_checkboxes = dict()

    # show container
    container = st.container(border=True)

    with container:
        # title
        st.markdown("<h4 style='text-align: center;'>최근에 만들었던 음식들을 골라주세요</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>5개 이상 선택해주세요</div>", unsafe_allow_html=True)

        for page_url in st.session_state['page_urls']:
            # 16개 이미지 렌더링
            checkboxes, next_page_url = show_recipes(page_url)
            # 16개에 대한 체크박스 추가
            all_checkboxes.update(checkboxes)

        # 5개 이상 체크했는지 확인
        if sum(all_checkboxes.values()) >= 5:
            checked_items = [recipe for recipe, checked in all_checkboxes.items() if checked]
        else:
            checked_items = []
#            st.markdown("<div style='text-align: center;'>⚠️추천 정확성을 위해 5개 이상 체크해주세요.</div>", unsafe_allow_html=True)
        if st.session_state['page_warn']:
            st.error("⚠️추천 정확성을 위해 5개 이상 체크해주세요.")

        if len(next_page_url):
            cols = st.columns([3,1,1.5,3])
            with cols[1]:
                st.button('더보기', on_click=add_next_page_url, kwargs=dict(next_page_url=next_page_url))
            with cols[2]:
                st.button('다음단계', type='primary', on_click=post_cooked_recipes, args=(checked_items, all_checkboxes))
        else:
            cols = st.columns([3,1,3])
            with cols[1]:
                st.button('다음단계', type='primary', on_click=post_cooked_recipes, args=(checked_items, all_checkboxes))

#def choose_food_page():
#
#    if not choose_food_container():
#        st.stop()
