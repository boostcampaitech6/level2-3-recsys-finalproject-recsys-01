import streamlit as st
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container
from st_supabase_connection import SupabaseConnection
from st_login_form import login_form
from streamlit_login_auth_ui.widgets import __login__
from pages import main_page, signin_page, main_page_2, user_history_page
# login_page, signin_page_2, signin_page_3, 

st.set_page_config(layout="wide")

app_title = "🛒 나만의 식량 바구니"
menu_titles = ["house", "🛒이번주 장바구니 추천", "😋내가 요리한 레시피", "🔎취향저격 레시피", "Log In / 회원가입", "MainPage-2"]
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
            ], align='center', use_container_width=True,
        )

    container2 = st.container(border=True)
    with container2:
        if seg == menu_titles[1]:
            # 🛒이번주 장바구니 추천
            container3 = st.container(border=True)
            with container3:
                st.markdown(f"<h4 style='text-align: center;'>{menu_titles[1]}</h4>", unsafe_allow_html=True)
        elif seg == menu_titles[2]:
            # 😋내가 요리한 레시피
            user_history_page()
        elif seg == menu_titles[3]:
            # 취향저격 레시피 
            # Test
            main_page_2()
        elif seg == menu_titles[4]:
            # 로그인 / 회원가입
            signin_page()
        elif seg == menu_titles[5]:
            # MainPage_2
            main_page_2()
        else :
            # Home
            main_page()
            
                    

# 버튼
# btn = sac.buttons(
#     items=['button1', 'button2', 'button3'],
#     index=0,
#     format_func='title',
#     align='center',
#     direction='horizontal',
#     radius='lg',
#     return_index=False,
# )
# st.write(f'The selected button label is: {btn}')