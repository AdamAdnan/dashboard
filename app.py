import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    return day, hour

day_df, hour_df = load_data()

st.title("🚲 Bike Sharing Dashboard")

# ======================
# Sidebar Filter
# ======================
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Select Year", ["All", 2011, 2012])

if year_filter != "All":
    year_val = 0 if year_filter == 2011 else 1
    day_df = day_df[day_df["yr"] == year_val]
    hour_df = hour_df[hour_df["yr"] == year_val]

# ======================
# KPI Row
# ======================
total_rent = hour_df["cnt"].sum()
total_casual = hour_df["casual"].sum()
total_registered = hour_df["registered"].sum()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Rentals", f"{total_rent:,}")
kpi2.metric("Casual Users", f"{total_casual:,}")
kpi3.metric("Registered Users", f"{total_registered:,}")

# ======================
# Row 1: Time + Segment
# ======================
col1, col2 = st.columns(2)

with col1:
    hourly_avg = hour_df.groupby("hr")["cnt"].mean()
    fig, ax = plt.subplots()
    hourly_avg.plot(ax=ax)
    ax.set_title("Average Rentals per Hour")
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.bar(["Casual", "Registered"], [total_casual, total_registered])
    ax2.set_title("Total Rentals by User Type")
    st.pyplot(fig2)

# ======================
# Row 2: User Pattern
# ======================
hourly_user = hour_df.groupby("hr")[["casual", "registered"]].mean()

fig3, ax3 = plt.subplots()
hourly_user.plot(ax=ax3)
ax3.set_title("Hourly Usage Pattern by User Type")
st.pyplot(fig3)

# ======================
# Row 3: Weather & Season
# ======================
col3, col4 = st.columns(2)

with col3:
    weather_avg = hour_df.groupby("weathersit")["cnt"].mean()
    fig4, ax4 = plt.subplots()
    weather_avg.plot(kind="bar", ax=ax4)
    ax4.set_title("Average Rentals by Weather")
    st.pyplot(fig4)

with col4:
    season_avg = day_df.groupby("season")["cnt"].mean()
    fig5, ax5 = plt.subplots()
    season_avg.plot(kind="bar", ax=ax5)
    ax5.set_title("Average Rentals by Season")
    st.pyplot(fig5)

# ======================
# Row 4: Clustering
# ======================
hour_cluster = hour_df.groupby("hr")["cnt"].mean().reset_index()
hour_cluster["level"] = pd.qcut(
    hour_cluster["cnt"], 3, labels=["Low", "Medium", "High"]
)

fig6, ax6 = plt.subplots()
for level in ["Low", "Medium", "High"]:
    subset = hour_cluster[hour_cluster["level"] == level]
    ax6.scatter(subset["hr"], subset["cnt"], label=level)

ax6.set_title("Demand Levels by Hour")
ax6.legend()
st.pyplot(fig6)
