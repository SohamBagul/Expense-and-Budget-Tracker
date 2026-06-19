from datetime import date

import pandas as pd
import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

CATEGORIES = [
    "Food", "Transport", "Shopping", "Entertainment",
    "Bills", "Healthcare", "Education", "Travel", "Other",
]

st.set_page_config(page_title="Budget Management", page_icon="🎯", layout="wide")

require_auth()
render_sidebar()

st.title("🎯 Budget Management")

token = get_token()

st.subheader("Set Monthly Budget")
with st.form("add_budget_form"):
    category = st.selectbox("Category", CATEGORIES)
    monthly_limit = st.number_input("Monthly Limit", min_value=0.01, step=0.01, format="%.2f")
    month = st.selectbox("Month", list(range(1, 13)), index=date.today().month - 1)
    year = st.number_input("Year", min_value=2000, max_value=2100, value=date.today().year)
    submitted = st.form_submit_button("Create Budget", use_container_width=True)

if submitted:
    payload = {
        "category": category,
        "monthly_limit": monthly_limit,
        "month": month,
        "year": year,
    }
    success, data = api_client.create_budget(token, payload)
    if success:
        st.success(f"Budget for '{data['category']}' created!")
        st.rerun()
    else:
        st.error(data)

st.divider()
st.subheader("Your Budgets")

success, budgets = api_client.get_budgets(token)
if not success:
    st.error(budgets)
    st.stop()

if not budgets:
    st.info("No budgets set yet.")
    st.stop()

df = pd.DataFrame(budgets)
st.dataframe(df, use_container_width=True, hide_index=True)

budget_options = {
    f"{b['id']} - {b['category']} ({b['month']}/{b['year']}) - ₹{b['monthly_limit']}": b
    for b in budgets
}
selected_label = st.selectbox("Select budget to edit/delete", list(budget_options.keys()))
selected = budget_options[selected_label]

with st.form("edit_budget_form"):
    edit_limit = st.number_input(
        "Monthly Limit",
        min_value=0.01,
        value=float(selected["monthly_limit"]),
        step=0.01,
        format="%.2f",
    )
    update_btn = st.form_submit_button("Update Budget", use_container_width=True)

if update_btn:
    ok, data = api_client.update_budget(token, selected["id"], {"monthly_limit": edit_limit})
    if ok:
        st.success("Budget updated successfully!")
        st.rerun()
    else:
        st.error(data)

if st.button("Delete Selected Budget", type="primary"):
    ok, err = api_client.delete_budget(token, selected["id"])
    if ok:
        st.success("Budget deleted successfully!")
        st.rerun()
    else:
        st.error(err)
