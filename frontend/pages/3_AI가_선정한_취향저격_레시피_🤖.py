import streamlit as st

from common import init, page_header, URL_MAIN, back_to_home_container
from recommendation_history import recommendation_history_page 
from streamlit_extras.switch_page_button import switch_page

# def back_to_home_container():
#     with st.container(border=True):
#         cols = st.columns([3,2,2])
#         with cols[1]:
#             st.write('로그인이 필요합니다.')
#         cols = st.columns([4,2.5,3])
#         with cols[1]:
#             # st.link_button('메인페이지로 >>', st.session_state.url_main, type='primary')
#             # st.link_button('메인페이지로 >>', st.session_state.get('url_main', URL_MAIN), type='primary')
#             if st.button('메인페이지로 >>', key='to_main'):
#                 switch_page('1_홈_🏠')
            
# if not st.session_state.is_authenticated:
if not st.session_state.get('is_authenticated', False):
    page_header(is_main=False)
    back_to_home_container()
else:
    page_header(is_main=False)
    recommendation_history_page()
