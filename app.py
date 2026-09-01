import sqlite3
import pandas as pd
import streamlit as st

# Configure Page Layout
st.set_page_config(
    page_title="Zaalima Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Engineering Analytics Dashboard")
st.markdown("Real-time metric visualization directly from `pipeline_staging.db`")

# Database Connection Helper
def get_connection():
    return sqlite3.connect("pipeline_staging.db")

# Fetch SQL View Data
@st.cache_data(ttl=600)
def load_view_data(view_name):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
    conn.close()
    return df

# Render UI
try:
    df_revenue = load_view_data("view_product_revenue")
    
    st.subheader("Product Revenue & Sales Performance")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(df_revenue, use_container_width=True)
        
    with col2:
        st.metric(
            label="Total Products Tracked", 
            value=len(df_revenue)
        )
        st.metric(
            label="Total Revenue", 
            value=f"${df_revenue['total_revenue'].sum():,.2f}" if 'total_revenue' in df_revenue.columns else "N/A"
        )

except Exception as e:
    st.error(f"Error loading database views: {e}")