import streamlit as st
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container
from streamlit_login_auth_ui.widgets import __login__
from utils import get_and_stack_recipe_data, get_my_recipe_data, page_header, display_ingredients_in_rows_of_four2, display_ingredients_in_rows_of_four, get_response, display_recipes_in_rows_of_four, basket_feedback

global api_prefix
api_prefix = "http://localhost:8000/"
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

def result_page_2():

    # 앱 헤더 
    page_header()

    url = api_prefix + "api/users/{user_id}/previousrecommendation"
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
