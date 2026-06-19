import streamlit as st

from services.api_client import api_client


def init_session_state() -> None:
    defaults = {
        "access_token": None,
        "refresh_token": None,
        "logged_in": False,
        "username": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_token() -> str | None:
    return st.session_state.get("access_token")


def require_auth() -> bool:
    init_session_state()
    if not st.session_state.get("logged_in") or not st.session_state.get("access_token"):
        st.warning("Please log in from the home page to access this section.")
        st.page_link("app.py", label="Go to Login", icon="🔐")
        st.stop()
    return True


def logout() -> None:
    token = st.session_state.get("access_token")
    if token:
        api_client.logout(token)
    st.session_state.access_token = None
    st.session_state.refresh_token = None
    st.session_state.logged_in = False
    st.session_state.username = None


def render_sidebar() -> None:
    with st.sidebar:
        st.title("💰 Expense Tracker")
        if st.session_state.get("logged_in"):
            st.success(f"Logged in as **{st.session_state.username}**")
            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.info("Not logged in")
