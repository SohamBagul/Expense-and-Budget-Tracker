from datetime import date

import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

CATEGORIES = [
    "Food", "Transport", "Shopping", "Entertainment",
    "Bills", "Healthcare", "Education", "Travel", "Other",
]

st.set_page_config(page_title="Add Expense", page_icon="➕", layout="wide")

require_auth()
render_sidebar()

st.title("➕ Add Expense")

token = get_token()

with st.form("add_expense_form"):
    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
    category = st.selectbox("Category", CATEGORIES)
    description = st.text_area("Description (optional)")
    expense_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Expense", use_container_width=True)

if submitted:
    if not title:
        st.error("Title is required.")
    else:
        payload = {
            "title": title,
            "amount": amount,
            "category": category,
            "description": description or None,
            "date": expense_date.isoformat(),
        }
        success, data = api_client.create_expense(token, payload)
        if success:
            st.success(f"Expense '{data['title']}' added successfully!")
        else:
            st.error(data)
