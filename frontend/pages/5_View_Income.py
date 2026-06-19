from datetime import date

import pandas as pd
import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

st.set_page_config(page_title="View Income", page_icon="💰", layout="wide")

require_auth()
render_sidebar()

st.title("💰 View Income")

token = get_token()
success, income_list = api_client.get_income(token)

if not success:
    st.error(income_list)
    st.stop()

if not income_list:
    st.info("No income records found. Add your first income entry!")
    st.stop()

df = pd.DataFrame(income_list)
st.dataframe(df[["id", "source", "amount", "date"]], use_container_width=True, hide_index=True)

st.divider()
st.subheader("Edit or Delete Income")

income_options = {f"{i['id']} - {i['source']} (₹{i['amount']})": i for i in income_list}
selected_label = st.selectbox("Select income", list(income_options.keys()))
selected = income_options[selected_label]

with st.form("edit_income_form"):
    edit_source = st.text_input("Source", value=selected["source"])
    edit_amount = st.number_input("Amount", min_value=0.01, value=float(selected["amount"]), step=0.01, format="%.2f")
    edit_date = st.date_input("Date", value=date.fromisoformat(selected["date"]))
    update_btn = st.form_submit_button("Update Income", use_container_width=True)

if update_btn:
    payload = {
        "source": edit_source,
        "amount": edit_amount,
        "date": edit_date.isoformat(),
    }
    ok, data = api_client.update_income(token, selected["id"], payload)
    if ok:
        st.success("Income updated successfully!")
        st.rerun()
    else:
        st.error(data)

if st.button("Delete Selected Income", type="primary"):
    ok, err = api_client.delete_income(token, selected["id"])
    if ok:
        st.success("Income deleted successfully!")
        st.rerun()
    else:
        st.error(err)
