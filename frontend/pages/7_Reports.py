from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

st.set_page_config(page_title="Reports", page_icon="📈", layout="wide")

require_auth()
render_sidebar()

st.title("📈 Reports")

token = get_token()

col1, col2 = st.columns(2)
with col1:
    month = st.selectbox("Month (for category report)", list(range(1, 13)), index=date.today().month - 1)
with col2:
    year = st.number_input("Year", min_value=2000, max_value=2100, value=date.today().year)

tab1, tab2, tab3 = st.tabs(["Monthly Report", "Category Report", "Income vs Expense"])

with tab1:
    st.subheader(f"Monthly Report — {year}")
    ok, data = api_client.get_monthly_report(token, year)
    if ok and data:
        df = pd.DataFrame(data)
        df["month_name"] = df["month"].apply(
            lambda m: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][m - 1]
        )
        st.dataframe(df[["month_name", "total_income", "total_expense", "balance"]], use_container_width=True, hide_index=True)
        fig = px.bar(
            df,
            x="month_name",
            y=["total_income", "total_expense"],
            barmode="group",
            title="Monthly Income vs Expense",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

with tab2:
    st.subheader(f"Category Report — {month}/{year}")
    ok, data = api_client.get_category_report(token, month, year)
    if ok and data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.pie(df, names="category", values="total_expense", title="Category Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No category data for this period.")

with tab3:
    st.subheader(f"Income vs Expense — {year}")
    ok, data = api_client.get_income_vs_expense(token, year)
    if ok and data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.line(
            df,
            x="month",
            y=["income", "expense"],
            title="Income vs Expense Trend",
            labels={"value": "Amount", "variable": "Type"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")
