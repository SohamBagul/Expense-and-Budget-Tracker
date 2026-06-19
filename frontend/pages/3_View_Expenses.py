from datetime import date

import pandas as pd
import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

CATEGORIES = [
    "Food", "Transport", "Shopping", "Entertainment",
    "Bills", "Healthcare", "Education", "Travel", "Other",
]

st.set_page_config(page_title="View Expenses", page_icon="📋", layout="wide")

require_auth()
render_sidebar()

st.title("📋 View Expenses")

token = get_token()
success, expenses = api_client.get_expenses(token)

if not success:
    st.error(expenses)
    st.stop()

if not expenses:
    st.info("No expenses found. Add your first expense!")
    st.stop()

df = pd.DataFrame(expenses)
st.dataframe(df[["id", "title", "amount", "category", "date", "description"]], use_container_width=True, hide_index=True)

st.divider()
st.subheader("Edit or Delete Expense")

expense_options = {f"{e['id']} - {e['title']} (₹{e['amount']})": e for e in expenses}
selected_label = st.selectbox("Select expense", list(expense_options.keys()))
selected = expense_options[selected_label]

with st.form("edit_expense_form"):
    edit_title = st.text_input("Title", value=selected["title"])
    edit_amount = st.number_input("Amount", min_value=0.01, value=float(selected["amount"]), step=0.01, format="%.2f")
    edit_category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(selected["category"]) if selected["category"] in CATEGORIES else 0)
    edit_description = st.text_area("Description", value=selected.get("description") or "")
    edit_date = st.date_input("Date", value=date.fromisoformat(selected["date"]))
    update_btn = st.form_submit_button("Update Expense", use_container_width=True)

if update_btn:
    payload = {
        "title": edit_title,
        "amount": edit_amount,
        "category": edit_category,
        "description": edit_description or None,
        "date": edit_date.isoformat(),
    }
    ok, data = api_client.update_expense(token, selected["id"], payload)
    if ok:
        st.success("Expense updated successfully!")
        st.rerun()
    else:
        st.error(data)

if st.button("Delete Selected Expense", type="primary"):
    ok, err = api_client.delete_expense(token, selected["id"])
    if ok:
        st.success("Expense deleted successfully!")
        st.rerun()
    else:
        st.error(err)
