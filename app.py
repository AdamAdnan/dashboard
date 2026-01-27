import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
# Sidebar Filters
# ======================
st.sidebar.header("Filters")

year_filter = st.sidebar.selectbox("Select Year", ["All", 2011, 2012])

if year_filter != "All":
    year_val = 0 if year_filter == 2011 else 1
    day_df = day_df[day_df["yr"] == year_val]
    hour_df = hour_df[hour_df["yr"] == year_val]

# ======================
# Tabs Layout
# ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Time Analysis",
    "User Analysis",
    "Weather & Season",
    "Demand Clustering"
])

# ======================
# TAB 1 — Overview
# ======================
with tab1:
    total_rent = hour_df["cnt"].sum()
    total_casual = hour_df["casual"].sum()
    total_registered = hour_df["registered"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rentals", f"{total_rent:,}")
    col2.metric("Casual Users", f"{total_casual:,}")
    col3.metric("Registered Users", f"{total_registered:,}")

# ======================
# TAB 2 — Time Analysis
# ======================
with tab2:
    hourly_avg = hour_df.groupby("hr")["cnt"].mean()

    fig, ax = plt.subplots()
    hourly_avg.plot(ax=ax)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Rentals")
    ax.set_title("Average Rentals per Hour")
    st.pyplot(fig)

# ======================
# TAB 3 — User Analysis
# ======================
with tab3:
    total_casual = hour_df["casual"].sum()
    total_registered = hour_df["registered"].sum()

    fig1, ax1 = plt.subplots()
    ax1.bar(["Casual", "Registered"], [total_casual, total_registered])
    ax1.set_title("Total Rentals by User Type")
    st.pyplot(fig1)

    hourly_user = hour_df.groupby("hr")[["casual", "registered"]].mean()

    fig2, ax2 = plt.subplots()
    hourly_user.plot(ax=ax2)
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Average Rentals")
    ax2.set_title("Hourly Usage Pattern by User Type")
    st.pyplot(fig2)

# ======================
# TAB 4 — Weather & Season
# ======================
with tab4:
    weather_avg = hour_df.groupby("weathersit")["cnt"].mean()

    fig3, ax3 = plt.subplots()
    weather_avg.plot(kind="bar", ax=ax3)
    ax3.set_title("Average Rentals by Weather Condition")
    st.pyplot(fig3)

    season_avg = day_df.groupby("season")["cnt"].mean()

    fig4, ax4 = plt.subplots()
    season_avg.plot(kind="bar", ax=ax4)
    ax4.set_title("Average Rentals by Season")
    st.pyplot(fig4)

# ======================
# TAB 5 — Demand Clustering
# ======================
with tab5:
    hour_cluster = hour_df.groupby("hr")["cnt"].mean().reset_index()
    hour_cluster["level"] = pd.qcut(
        hour_cluster["cnt"], 3, labels=["Low", "Medium", "High"]
    )

    fig5, ax5 = plt.subplots()

    for level in ["Low", "Medium", "High"]:
        subset = hour_cluster[hour_cluster["level"] == level]
        ax5.scatter(subset["hr"], subset["cnt"], label=level)

    ax5.set_xlabel("Hour")
    ax5.set_ylabel("Average Rentals")
    ax5.set_title("Demand Levels by Hour")
    ax5.legend()

    st.pyplot(fig5)
