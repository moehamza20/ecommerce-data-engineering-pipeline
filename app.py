
import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import get_warehouse_connection

st.set_page_config(
    page_title="E-Commerce Data Warehouse",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Analytics Dashboard")
st.caption("Sales insights powered by PostgreSQL and Python ETL")


@st.cache_data(ttl=60)
def load_data(query):
    conn = get_warehouse_connection()
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


try:
    # KPI metrics
    kpis = load_data("""
        SELECT
            COALESCE(SUM(total_amount), 0) AS total_revenue,
            COUNT(DISTINCT order_id) AS completed_orders,
            COUNT(DISTINCT customer_key) AS purchasing_customers
        FROM fact_sales
        WHERE order_status = 'completed'
    """)

    aov = load_data("""
        SELECT COALESCE(AVG(order_total), 0) AS average_order_value
        FROM (
            SELECT order_id, SUM(total_amount) AS order_total
            FROM fact_sales
            WHERE order_status = 'completed'
            GROUP BY order_id
        ) orders
    """)

    revenue = float(kpis.iloc[0]["total_revenue"])
    completed_orders = int(kpis.iloc[0]["completed_orders"])
    customers = int(kpis.iloc[0]["purchasing_customers"])
    average_order_value = float(aov.iloc[0]["average_order_value"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Completed Revenue", f"{revenue:,.2f}")
    col2.metric("Completed Orders", f"{completed_orders:,}")
    col3.metric("Average Order Value", f"{average_order_value:,.2f}")
    col4.metric("Purchasing Customers", f"{customers:,}")

    st.divider()

    # Monthly revenue chart
    monthly = load_data("""
        SELECT
            d.year,
            d.month,
            TO_CHAR(
                MAKE_DATE(d.year, d.month, 1),
                'Mon YYYY'
            ) AS month_label,
            SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_date d ON fs.date_key = d.date_key
        WHERE fs.order_status = 'completed'
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month
    """)

    # Category revenue chart
    categories = load_data("""
        SELECT
            p.category,
            SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_product p ON fs.product_key = p.product_key
        WHERE fs.order_status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC
    """)

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly Revenue")
        if not monthly.empty:
            fig = px.line(
                monthly,
                x="month_label",
                y="revenue",
                markers=True,
                labels={
                    "month_label": "Month",
                    "revenue": "Revenue"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No completed sales data available.")

    with right:
        st.subheader("Revenue by Category")
        if not categories.empty:
            fig = px.bar(
                categories,
                x="category",
                y="revenue",
                labels={
                    "category": "Category",
                    "revenue": "Revenue"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No completed sales data available.")

    # Top products
    st.divider()
    left, right = st.columns(2)

    products = load_data("""
        SELECT
            p.name AS product_name,
            SUM(fs.quantity) AS units_sold,
            SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_product p ON fs.product_key = p.product_key
        WHERE fs.order_status = 'completed'
        GROUP BY p.product_key, p.name
        ORDER BY revenue DESC
        LIMIT 5
    """)

    customers_table = load_data("""
        SELECT
            c.name AS customer_name,
            COUNT(DISTINCT fs.order_id) AS completed_orders,
            SUM(fs.total_amount) AS total_spent
        FROM fact_sales fs
        JOIN dim_customer c ON fs.customer_key = c.customer_key
        WHERE fs.order_status = 'completed'
        GROUP BY c.customer_key, c.name
        ORDER BY total_spent DESC
        LIMIT 5
    """)

    with left:
        st.subheader("Top 5 Products")
        st.dataframe(products, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Top 5 Customers")
        st.dataframe(customers_table, use_container_width=True, hide_index=True)

except Exception as error:
    st.error(
        "Could not load dashboard data. Check your PostgreSQL "
        "connection settings and confirm that the ETL pipeline has run."
    )
    st.exception(error)
