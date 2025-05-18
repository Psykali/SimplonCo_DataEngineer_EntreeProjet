# dashboard.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Database connection
conn = sqlite3.connect('data/sales.db')

# Total revenue
total_revenue = pd.read_sql("SELECT SUM(amount) FROM sales", conn).iloc[0,0]

# Top products
product_sales = pd.read_sql('''
  SELECT p.name, SUM(s.amount) as revenue 
  FROM sales s JOIN products p ON s.product_id = p.id 
  GROUP BY p.name ORDER BY revenue DESC LIMIT 5
''', conn)

# Streamlit Dashboard
st.title("📈 Sales Dashboard")
st.metric("Total Revenue", f"€{total_revenue:,.2f}")

col1, col2 = st.columns(2)
with col1:
    st.header("Top 5 Products")
    fig = px.bar(product_sales, x="name", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Sales by Region")
    region_data = pd.read_sql('''
      SELECT st.region, SUM(s.amount) as revenue 
      FROM sales s JOIN stores st ON s.store_id = st.id 
      GROUP BY st.region
    ''', conn)
    fig = px.pie(region_data, values="revenue", names="region")
    st.plotly_chart(fig, use_container_width=True)
