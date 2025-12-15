import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# TITLE
st.title("📊 Sales Data Dashboard (Python + Streamlit)")
st.write("Analyze sales trends & patterns with uploaded or sample generated data.")


# CSV UPLOAD 
st.subheader("📂 Upload Your Own Sales CSV File")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# LOAD DATA 
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.subheader("Generate Sample Sales Data")

    num_rows = st.slider(
        "Select number of sample rows", min_value=50, max_value=1000, value=300
    )

    np.random.seed(42)
    data = pd.DataFrame({
        "InvoiceDate": pd.date_range(start="2024-01-01", periods=num_rows, freq="D"),
        "Region": np.random.choice(["North", "South", "East", "West"], num_rows),
        "Product": np.random.choice(["Laptop", "Headphones", "Mobile", "Camera"], num_rows),
        "Sales": np.random.randint(2000, 50000, num_rows)
    })


# DISPLAY TABLE 
st.subheader("📋 Sales Dataset Preview")
st.dataframe(data, use_container_width=True)


# FILTERS 
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

# KPI METRICS 
st.subheader("📌 Key Metrics")

total_sales = filtered_data["Sales"].sum()
avg_sales = filtered_data["Sales"].mean()
max_sales = filtered_data["Sales"].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{total_sales:,}")
col2.metric("Average Sale", f"{avg_sales:,.2f}")
col3.metric("Max Sale", f"{max_sales:,}")


# SALES TREND (Altair)
st.subheader("📈 Sales Trend Over Time")

sales_trend = filtered_data.groupby("InvoiceDate")["Sales"].sum().reset_index()

line_chart = alt.Chart(sales_trend).mark_line(point=True).encode(
    x="InvoiceDate:T",
    y="Sales:Q",
    tooltip=["InvoiceDate", "Sales"]
).interactive()

st.altair_chart(line_chart, use_container_width=True)


# SALES BY REGION (BAR CHART)
st.subheader("📊 Sales by Region")

region_sales = filtered_data.groupby("Region")["Sales"].sum()

fig1, ax1 = plt.subplots()
ax1.bar(region_sales.index, region_sales.values)
ax1.set_xlabel("Region")
ax1.set_ylabel("Total Sales")
ax1.set_title("Total Sales by Region")

st.pyplot(fig1)


# SALES BY PRODUCT (BAR CHART)
st.subheader("📦 Sales by Product")

product_sales = filtered_data.groupby("Product")["Sales"].sum()

fig2, ax2 = plt.subplots()
ax2.bar(product_sales.index, product_sales.values)
ax2.set_xlabel("Product")
ax2.set_ylabel("Total Sales")
ax2.set_title("Total Sales by Product")

st.pyplot(fig2)


# DOWNLOAD FILTERED DATA
st.subheader("⬇️ Download Filtered CSV")

csv = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)
