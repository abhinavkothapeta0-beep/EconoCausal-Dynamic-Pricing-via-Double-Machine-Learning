import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Electricity Consumption Dashboard",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# Sample data (replace with your CSV later)
# -----------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", periods=180, freq="D")
    data = pd.DataFrame({
        "Date": dates,
        "Consumption (kWh)": np.random.normal(420, 65, len(dates)).clip(220, 650),
        "Temperature (°C)": np.random.normal(29, 4, len(dates)).clip(18, 40),
        "Region": np.random.choice(["North", "South", "East", "West"], len(dates)),
        "Peak Load (kW)": np.random.normal(95, 14, len(dates)).clip(50, 140)
    })
    data["Month"] = data["Date"].dt.strftime("%b")
    return data

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("Dashboard Filters")
regions = st.sidebar.multiselect(
    "Select region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

date_range = st.sidebar.date_input(
    "Select date range",
    value=(df["Date"].min().date(), df["Date"].max().date()),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

filtered = df[df["Region"].isin(regions)].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["Date"].dt.date >= start_date) &
        (filtered["Date"].dt.date <= end_date)
    ]

# -----------------------------
# Dashboard
# -----------------------------
st.title("⚡ Electricity Consumption Dashboard")
st.caption("Sample dashboard using generated electricity data. Replace the sample data with your project dataset when ready.")

if filtered.empty:
    st.warning("No records match the selected filters. Please change the filters.")
    st.stop()

total_consumption = filtered["Consumption (kWh)"].sum()
average_daily = filtered["Consumption (kWh)"].mean()
max_peak = filtered["Peak Load (kW)"].max()
average_temperature = filtered["Temperature (°C)"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Consumption", f"{total_consumption:,.0f} kWh")
col2.metric("Average Daily Use", f"{average_daily:,.1f} kWh")
col3.metric("Maximum Peak Load", f"{max_peak:,.1f} kW")
col4.metric("Average Temperature", f"{average_temperature:.1f} °C")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Daily Electricity Consumption")
    daily = filtered.groupby("Date", as_index=False)["Consumption (kWh)"].sum()
    fig_daily = px.line(
        daily, x="Date", y="Consumption (kWh)",
        markers=True, title="Consumption over time"
    )
    st.plotly_chart(fig_daily, use_container_width=True)

with right:
    st.subheader("Consumption by Region")
    region_data = filtered.groupby("Region", as_index=False)["Consumption (kWh)"].sum()
    fig_region = px.bar(
        region_data, x="Region", y="Consumption (kWh)",
        color="Region", title="Total consumption by region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Temperature vs. Consumption")
    fig_scatter = px.scatter(
        filtered, x="Temperature (°C)", y="Consumption (kWh)",
        color="Region", title="Relationship between temperature and usage"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with right:
    st.subheader("Peak Load Distribution")
    fig_hist = px.histogram(
        filtered, x="Peak Load (kW)", nbins=20,
        title="Distribution of peak load"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Filtered Dataset")
st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="electricity_dashboard_data.csv",
    mime="text/csv"
)
