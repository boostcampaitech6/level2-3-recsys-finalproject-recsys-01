import streamlit as st
import requests

def login_request(user_id, password):
    
    full_url = st.session_state.url_prefix + '/api/users/auths'

    request_body = {
        'login_id': user_id,
        'password': password,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(full_url, headers=headers, json=request_body)
    response_json = response.json() if response.status_code == 200 else None

    return response.status_code, response_json

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="user_id")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # api 기준으로 바꿔보자
        input_user_id = st.session_state['user_id']
        input_password = st.session_state['password']

        status_code, response = login_request(input_user_id, input_password)

        if status_code == 200:
            # 페이지 전환을 위해
            if 'recommendation_result' in st.session_state:
                del st.session_state['recommendation_result']
            st.session_state["password_correct"] = True
            st.session_state.is_authenticated = True
            st.session_state.page_info = 'home2'
            st.session_state["token"] = {
                'user_id': st.session_state['user_id'],
                'token': response['token'], 
                'is_first_login': response['is_first_login']
            }

            del st.session_state["password"]  # Don't store the user_id or password.

        else:
            st.session_state["password_correct"] = False

            if status_code == 400:
                st.session_state.msg = "password incorrect"
            elif status_code == 404:
                st.session_state.msg = "User not known"
            else:
                st.session_state.msg = "Server Error"



    # Return True if the user_id + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for user_id + password.
    login_form()

    if "password_correct" in st.session_state:
        st.error(f"😕 {st.session_state.msg}")
    return False


def login_container():
    if not check_password():
        st.stop()
