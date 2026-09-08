import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "pipeline_staging.db"
LOG_PATH = "pipeline_execution.log"

st.set_page_config(
    page_title="Zaalima Data Engine Dashboard",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Zaalima Data Engine - Operational Dashboard")
st.markdown("---")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Overview", "Product Revenue Analysis", "Customer Insights", "System Logs"],
)


def get_connection():
    return sqlite3.connect(DB_PATH)


# Page 1: Overview
if page == "Overview":
    st.subheader("📌 System Summary")
    if os.path.exists(DB_PATH):
        conn = get_connection()
        try:
            total_orders = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM staging_orders;", conn
            ).iloc[0]["count"]
            st.metric("Total Staging Orders Processed", f"{total_orders:,}")
            st.success("Database Connection: Active")
        except Exception as e:
            st.error(f"Error reading staging data: {e}")
        finally:
            conn.close()
    else:
        st.warning(
            "Database file `pipeline_staging.db` not found. Run `main.py` first."
        )

# Page 2: Product Revenue Analysis
elif page == "Product Revenue Analysis":
    st.subheader("📊 Product Revenue View")
    if os.path.exists(DB_PATH):
        conn = get_connection()
        df_revenue = pd.read_sql_query(
            "SELECT * FROM view_product_revenue;", conn
        )
        conn.close()

        if not df_revenue.empty:
            st.dataframe(df_revenue, use_container_width=True)
            st.bar_chart(
                df_revenue.set_index(df_revenue.columns[0])[
                    df_revenue.columns[1]
                ]
            )
        else:
            st.info("No data in `view_product_revenue`.")
    else:
        st.warning("Database not found.")

# Page 3: Customer Insights
elif page == "Customer Insights":
    st.subheader("👥 Customer Summary View")
    if os.path.exists(DB_PATH):
        conn = get_connection()
        df_customer = pd.read_sql_query(
            "SELECT * FROM view_customer_summary;", conn
        )
        conn.close()

        if not df_customer.empty:
            st.dataframe(df_customer, use_container_width=True)
        else:
            st.info("No data in `view_customer_summary`.")
    else:
        st.warning("Database not found.")

# Page 4: System Logs
elif page == "System Logs":
    st.subheader("📜 Live System Logs")
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = f.readlines()
        st.code("".join(logs[-50:]), language="log")
    else:
        st.info("No log file found yet.")