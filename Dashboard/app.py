import streamlit as st
from Dashboard.utils import get_database_connection,fetch_data

st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Data Analytics Dashboard")

st.sidebar.header("Dashboard Filters")
st.sidebar.info("Filters will be added here.")
# Main dashboard tabs
tab1, tab2, tab3 = st.tabs([
    "Executive Overview",
    "Detailed Analytics",
    "Data Quality"
])

with tab1:
    st.header("Executive Overview")
    st.info("Executive metrics and summary charts will be displayed here.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", "1,250")

    with col2:
        st.metric("Total Revenue", "₹2.5L")

    with col3:
        st.metric("Data Quality", "95%")

with tab2:
    st.header("Detailed Analytics")
    st.info("Detailed charts and analytics will be added here.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Trend Analysis")
        st.line_chart([10, 20, 15, 30, 25])

    with col2:
        st.subheader("Distribution")
        st.bar_chart([20, 35, 25, 40])

with tab3:
    st.header("Data Quality")
    st.info("Data quality checks will be added here.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Missing Values", "5%")

    with col2:
        st.metric("Duplicate Records", "12")