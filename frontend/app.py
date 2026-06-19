import streamlit as st

from services.api_client import api_client
from services.auth_utils import init_session_state, logout, render_sidebar

st.set_page_config(
    page_title="Expense Tracker - Login",
    page_icon="💰",
    layout="wide",
)

init_session_state()
render_sidebar()

st.title("💰 Expense Tracking & Budget Management")
st.markdown("Track expenses, manage income, set budgets, and view financial reports.")

if st.session_state.get("logged_in"):
    st.success(f"Welcome back, **{st.session_state.username}**!")
    st.info("Use the sidebar to navigate to Dashboard, Expenses, Income, Budget, and Reports.")
    if st.button("Logout"):
        logout()
        st.rerun()
else:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login to your account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter username and password.")
            else:
                success, data = api_client.login(username, password)
                if success:
                    st.session_state.access_token = data["access_token"]
                    st.session_state.refresh_token = data["refresh_token"]
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(data)

    with tab_register:
        st.subheader("Create a new account")
        with st.form("register_form"):
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            reg_submitted = st.form_submit_button("Register", use_container_width=True)

        if reg_submitted:
            if not reg_username or not reg_email or not reg_password:
                st.error("Please fill in all fields.")
            elif reg_password != reg_confirm:
                st.error("Passwords do not match.")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                success, data = api_client.register(reg_username, reg_email, reg_password)
                if success:
                    st.success("Registration successful! Please log in.")
                else:
                    st.error(data)
