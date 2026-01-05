import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Sales Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------- TITLE --------------------
st.title("📊 Sales Data Dashboard (Python + Streamlit)")
st.write("Analyze sales trends & patterns using uploaded or sample-generated data.")

# -------------------- CSV UPLOAD --------------------
st.subheader("📂 Upload Your Own Sales CSV File")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# -------------------- LOAD DATA --------------------
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.subheader("Generate Sample Sales Data")

    num_rows = st.slider(
        "Select number of sample rows",
        min_value=50,
        max_value=1000,
        value=300
    )

    np.random.seed(42)
    data = pd.DataFrame({
        "InvoiceDate": pd.date_range(start="2024-01-01", periods=num_rows, freq="D"),
        "Region": np.random.choice(["North", "South", "East", "West"], num_rows),
        "Product": np.random.choice(
            ["Laptop", "Headphones", "Mobile", "Camera"], num_rows
        ),
        "Sales": np.random.randint(2000, 50000, num_rows)
    })

# -------------------- DATA PREVIEW --------------------
st.subheader("📋 Sales Dataset Preview")
st.dataframe(data, use_container_width=True)

# -------------------- FILTERS --------------------
st.subheader("🔍 Data Filters")

region_filter = st.multiselect(
    "Filter by Region",
    options=data["Region"].unique(),
    default=data["Region"].unique()
)

product_filter = st.multiselect(
    "Filter by Product",
    options=data["Product"].unique(),
    default=data["Product"].unique()
)

filtered_data = data[
    (data["Region"].isin(region_filter)) &
    (data["Product"].isin(product_filter))
]

st.write(f"Total Rows after filter: **{len(filtered_data)}**")
st.dataframe(filtered_data, use_container_width=True)

# -------------------- KPI METRICS --------------------
st.subheader("📌 Key Metrics")

total_sales = filtered_data["Sales"].sum()
avg_sales = filtered_data["Sales"].mean()
max_sales = filtered_data["Sales"].max()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{total_sales:,}")
col2.metric("Average Sale", f"{avg_sales:,.2f}")
col3.metric("Max Sale", f"{max_sales:,}")

# -------------------- SALES TREND --------------------
st.subheader("📈 Sales Trend Over Time")

sales_trend = (
    filtered_data.groupby("InvoiceDate", as_index=False)["Sales"].sum()
)

trend_chart = alt.Chart(sales_trend).mark_line(point=True).encode(
    x=alt.X("InvoiceDate:T", title="Date"),
    y=alt.Y("Sales:Q", title="Total Sales"),
    tooltip=["InvoiceDate", "Sales"]
).interactive()

st.altair_chart(trend_chart, use_container_width=True)

# -------------------- SALES BY REGION --------------------
st.subheader("📊 Sales by Region")

region_sales = (
    filtered_data.groupby("Region", as_index=False)["Sales"].sum()
)

region_chart = alt.Chart(region_sales).mark_bar().encode(
    x=alt.X("Region:N", title="Region"),
    y=alt.Y("Sales:Q", title="Total Sales"),
    tooltip=["Region", "Sales"]
)

st.altair_chart(region_chart, use_container_width=True)

# -------------------- SALES BY PRODUCT --------------------
st.subheader("📦 Sales by Product")

product_sales = (
    filtered_data.groupby("Product", as_index=False)["Sales"].sum()
)

product_chart = alt.Chart(product_sales).mark_bar().encode(
    x=alt.X("Product:N", title="Product"),
    y=alt.Y("Sales:Q", title="Total Sales"),
    tooltip=["Product", "Sales"]
)

st.altair_chart(product_chart, use_container_width=True)

# -------------------- DOWNLOAD CSV --------------------
st.subheader("⬇️ Download Filtered Data")

csv = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)
