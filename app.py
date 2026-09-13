import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Zaalima Data Analytics Engine", layout="wide")

st.title("📊 Zaalima Data Analytics Engine")

# Fetch data from staging database
@st.cache_data
def load_data():
    conn = sqlite3.connect("pipeline_staging.db")
    df_revenue = pd.read_sql_query("SELECT * FROM view_product_revenue", conn)
    df_customers = pd.read_sql_query("SELECT * FROM view_customer_summary", conn)
    conn.close()
    return df_revenue, df_customers

try:
    df_rev, df_cust = load_data()

    # KPI Summary Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", len(df_rev))
    col2.metric("Total Customers", len(df_cust))
    col3.metric("Total Revenue ($)", f"${df_rev['total_revenue'].sum():,.2f}")

    st.markdown("---")

    # Analytical Charts Section
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("Product Revenue Performance")
        fig, ax = plt.subplots()
        sns.barplot(data=df_rev, x="total_revenue", y="product_name", ax=ax, palette="Blues_r")
        ax.set_xlabel("Revenue ($)")
        ax.set_ylabel("Product")
        st.pyplot(fig)

    with right_chart:
        st.subheader("Customer Spend Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(df_cust["total_spend"], kde=True, ax=ax2, color="skyblue")
        ax2.set_xlabel("Total Spend ($)")
        st.pyplot(fig2)

except Exception as e:
    st.error(f"Please run 'py main.py' first to generate pipeline_staging.db! Error: {e}")