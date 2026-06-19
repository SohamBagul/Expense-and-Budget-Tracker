from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from services.api_client import api_client
from services.auth_utils import get_token, render_sidebar, require_auth

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

require_auth()
render_sidebar()

st.title("📊 Dashboard")

token = get_token()
col1, col2 = st.columns(2)
with col1:
    month = st.selectbox("Month", list(range(1, 13)), index=date.today().month - 1)
with col2:
    year = st.number_input("Year", min_value=2000, max_value=2100, value=date.today().year)

success, summary = api_client.get_dashboard_summary(token, month, year)
if not success:
    st.error(summary)
    st.stop()

m1, m2, m3 = st.columns(3)
m1.metric("Total Income", f"₹{summary['total_income']:,.2f}")
m2.metric("Total Expense", f"₹{summary['total_expense']:,.2f}")
m3.metric("Remaining Balance", f"₹{summary['remaining_balance']:,.2f}")

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Expense by Category")
    ok_cat, category_data = api_client.get_category_wise(token, month, year)
    if ok_cat and category_data:
        df_cat = pd.DataFrame(category_data)
        fig_pie = px.pie(df_cat, names="category", values="total", title="Category-wise Expenses")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No expense data for this period.")

with chart_col2:
    st.subheader("Monthly Expenses")
    ok_monthly, monthly_data = api_client.get_monthly_expenses(token, year)
    if ok_monthly and monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        fig_bar = px.bar(df_monthly, x="month", y="total", title=f"Monthly Expenses ({year})")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No monthly expense data.")

st.subheader("Income vs Expense Trend")
ok_trend, trend_data = api_client.get_income_vs_expense(token, year)
if ok_trend and trend_data:
    df_trend = pd.DataFrame(trend_data)
    fig_line = px.line(
        df_trend,
        x="month",
        y=["income", "expense"],
        title=f"Income vs Expense ({year})",
        labels={"value": "Amount", "variable": "Type"},
    )
    st.plotly_chart(fig_line, use_container_width=True)

if summary.get("budget_usage"):
    st.subheader("Budget Usage")
    df_budget = pd.DataFrame(summary["budget_usage"])
    st.dataframe(df_budget, use_container_width=True, hide_index=True)

    fig_budget = px.bar(
        df_budget,
        x="category",
        y="usage_percentage",
        title="Budget Usage Percentage",
        labels={"usage_percentage": "Usage %"},
    )
    st.plotly_chart(fig_budget, use_container_width=True)
