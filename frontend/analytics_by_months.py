import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")

    # ✅ Check API response
    if response.status_code != 200:
        st.error("Failed to fetch monthly summary")
        return

    monthly_summary = response.json()

    # ✅ Create DataFrame
    df = pd.DataFrame(monthly_summary)

    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)

    # ✅ Sort
    df_sorted = df.sort_values(by="Month Number")

    st.title("Expense Breakdown By Months")

    # ✅ Chart (NO double set_index)
    chart_df = df_sorted.set_index("Month Name")[["Total"]]
    st.bar_chart(chart_df, use_container_width=True)

    # ✅ Format numbers AFTER chart
    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

    # ✅ Table
    st.table(df_sorted.set_index("Month Number"))
