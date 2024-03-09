import streamlit as st

def menu_tab(login=False, user=None):
    # layout
    cols = st.columns([1,2])

    with cols[0]:
        st.markdown('<button class="button0">🛒나만의 식량 바구니</button>', unsafe_allow_html=True)

    with cols[1]:
        cols2 = st.columns([5,5,4,4])
        with cols2[0]:
            st.markdown('<button class="button1">🛒이번주 장바구니 추천</button>', unsafe_allow_html=True)
        with cols2[1]:
            st.markdown('<button class="button1">😋내가 요리한 레시피</button>', unsafe_allow_html=True)
        with cols2[2]:
            st.markdown('<button class="button1">🔎취향저격 레시피</button>', unsafe_allow_html=True)
        with cols2[3]:
            if login:
                st.markdown(f'<button class="button1">{user}님 | 로그아웃</button>', unsafe_allow_html=True)
            else:
                st.markdown(f'<button class="button1">회원가입 | 로그인</button>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .button0 {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
            font-size: 24px;
            font-weight: bolder;
            cursor: pointer;
            border: none !important;
            vertical-align: middle;
        }
        .button1 {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
            font-size: 12px;
            cursor: pointer;
            border: none !important;
            vertical-align: middle;
        }
        /*
        button:hover {
            text-decoration: none;
            color: black !important;
        }
        button:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        */
        </style>
        """,
        unsafe_allow_html=True,
    )
