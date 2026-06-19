from datetime import date

import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

st.set_page_config(page_title="Add Income", page_icon="💵", layout="wide")

require_auth()
render_sidebar()

st.title("💵 Add Income")

token = get_token()

with st.form("add_income_form"):
    source = st.text_input("Source (e.g. Salary, Freelance)")
    amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
    income_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Income", use_container_width=True)

if submitted:
    if not source:
        st.error("Source is required.")
    else:
        payload = {
            "source": source,
            "amount": amount,
            "date": income_date.isoformat(),
        }
        success, data = api_client.create_income(token, payload)
        if success:
            st.success(f"Income from '{data['source']}' added successfully!")
        else:
            st.error(data)
