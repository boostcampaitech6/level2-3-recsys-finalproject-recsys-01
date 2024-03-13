import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import streamlit_antd_components as sac
from streamlit_login_auth_ui.widgets import __login__

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
    container3 = st.container(border=True)
    with container3:
        st.markdown("<h4 style='text-align: center;'>최근에 만들었던 음식을 골라주세요</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>5개 이상 선택해 주세요</p>", unsafe_allow_html=True)
        cols2 = st.columns([4,4])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col2:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col3:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col4:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
                
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col6:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col7:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col8:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        
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
    
    
    # 이번주 식량 바구니 추천    
    container3_2 = st.container(border = True)
    with container3_2:
        st.markdown("<h4 style='text-align: center;'>이번주 식량 바구니 추천  </h4>", unsafe_allow_html=True)
        
        col_left, col_1, col_2, col_3, col_4, col_5, col_right = st.columns((1, 1, 1, 1, 1, 1, 1))
        
        with col_1:
            st.image('img/potato.png')
        with col_2:
            st.image('img/potato.png')
        with col_3:
            st.image('img/potato.png')
        with col_4:
            st.image('img/potato.png')
        with col_5:
            st.image('img/potato.png')
    
    # 취향저격 레시피

    container3_3 = st.container(border = True)
    with container3_3:
        st.markdown("<h4 style='text-align: left;'>취향저격 레시피  </h4>", unsafe_allow_html=True)
        #### 
        st.page_link("pages/RecommendationPage.py", label="더 보기", icon="😎")
        #### 
        
        
        col_1, col_2, col_3, col_4, col_5 = st.columns((1, 1, 1, 1, 1))
        
        with col_1:
            st.image('img/potato.png')
        with col_2:
            st.image('img/potato.png')
        with col_3:
            st.image('img/potato.png')
        with col_4:
            st.image('img/potato.png')
        with col_5:
            st.image('img/potato.png')
    # 취향저격 레시피
    container3_4 = st.container(border = True)
    with container3_3:
        st.markdown("<h4 style='text-align: left;'>내가 해먹은 레시피  </h4>", unsafe_allow_html=True)
        
        col_1, col_2, col_3, col_4, col_5 = st.columns((1, 1, 1, 1, 1))
        
        with col_1:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col_2:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col_3:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col_4:
            with st.container(border=True):
                #col_l, col_c, 
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
        with col_5:
            with st.container(border=True):
                st.image("img/food.png")
                st.markdown("<p style='text-align: center;'>양배추 참치 덮밥</p>", unsafe_allow_html=True)
    