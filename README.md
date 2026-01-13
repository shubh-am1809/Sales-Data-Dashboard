# Sales Data Dashboard (Streamlit)

# Overview
This project is an interactive Sales Data Dashboard built using Python and Streamlit.
It allows users to analyze sales trends, regional performance, and product-wise sales using either uploaded CSV data or auto-generated sample data.

The dashboard provides real-time filtering, visualizations, KPIs, and data export capabilities for easy business analysis.

# Features
- Upload your own CSV sales data
- Generate sample sales data dynamically
- Interactive filters by Region and Product

# Key Performance Indicators (KPIs):
  - Total Sales
  - Average Sale
  - Maximum Sale

# Visualizations:
  - Sales trend over time (Line chart)
  - Sales by region (Bar chart)
  - Sales by product (Bar chart)
  - Download filtered data as CSV

# Dataset Structure
If uploading your own CSV file, it should contain the following columns:

| Column Name   | Description |
|--------------|------------|
| InvoiceDate  | Date of sale |
| Region       | Sales region (North, South, East, West) |
| Product      | Product name |
| Sales        | Sales amount |

# Technologies Used
- Python 3
- Streamlit – Web app framework
- Pandas – Data manipulation
- NumPy – Sample data generation
- Altair – Interactive charts
- Matplotlib– Bar charts




