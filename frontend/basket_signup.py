import hmac
import streamlit as st
import requests

def signup_request(username, nickname, email, password):
    
    full_url = st.session_state.url_prefix + '/api/users'

    request_body = {
        'login_id': username,
        'password': password,
        'nickname': nickname,
        'email': email,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(full_url, headers=headers, json=request_body)
    response_json = response.json() if response.status_code == 200 else None

    if response.status_code != 200:
        st.session_state.msg = eval(response.text)['detail']

    return response.status_code, response_json

def check_password():
    """Returns `True` if the user had a correct password."""

    def signup_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("login_id", key="login_id")
            st.text_input("nickname", key="nickname")
            st.text_input("email", key="email")
            st.text_input("password", type="password", key="password")
            st.form_submit_button("회원가입", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""

        status_code, response = signup_request(
            st.session_state['login_id'],
            st.session_state['nickname'],
            st.session_state['email'],
            st.session_state['password'],
        )

        if status_code == 200:

            st.session_state["signup_success"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["login_id"]  # Don't store the username or password.
            del st.session_state["nickname"]  # Don't store the username or password.
            del st.session_state["email"]  # Don't store the username or password.

        else:
            st.session_state["signup_success"] = False 

    # Return True if the username + password is validated.
    if st.session_state.get("signup_success", False):
        del st.session_state["signup_success"]
        return True

    # Show inputs for username + password.
    signup_form()

    if "signup_success" in st.session_state:
        st.error(f"😕 {st.session_state.msg}")
    return False

def signup_container():
    if not check_password():
        st.stop()

    # Main Streamlit app starts here
    st.session_state.page_info = 'home'
#    st.write(f"signup succeeded")
#    st.button("Click me")
