# Temporal Entrypoint
import streamlit as st

from utils import menu_tab

# page labeling
st.set_page_config(
    page_title="Entrypoint",
    page_icon="🛒",
)


# 상단 메뉴
menu_tab(login=True, user='Judy')
