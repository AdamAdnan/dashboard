import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    return day, hour

day_df, hour_df = load_data()

st.title("🚲 Bike Sharing Analysis Dashboard")

# ======================
# Sidebar Filter
# ======================
st.sidebar.header("Filter Data")

year_filter = st.sidebar.selectbox("Select Year", ["All", 2011, 2012])

if year_filter != "All":
    year_val = 0 if year_filter == 2011 else 1
    hour_df = hour_df[hour_df["yr"] == year_val]
    day_df = day_df[day_df["yr"] == year_val]

# ======================
# Business Overview
# ======================
st.header("Business Overview")

total_rent = hour_df["cnt"].sum()
total_casual = hour_df["casual"].sum()
total_registered = hour_df["registered"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{total_rent:,}")
col2.metric("Casual Users", f"{total_casual:,}")
col3.metric("Registered Users", f"{total_registered:,}")

st.divider()

# ======================
# Q1: Peak Hour Analysis
# ======================
st.header("Q1. Optimal Operational Time")

hourly_avg = hour_df.groupby("hr")["cnt"].mean()

fig, ax = plt.subplots()
hourly_avg.plot(ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Average Rentals")
ax.set_title("Average Rentals per Hour")
st.pyplot(fig)

st.write("""
Insight:
- Terlihat puncak peminjaman terjadi pada jam pagi dan sore hari.
- Ini menunjukkan pola commuting (pergi dan pulang kerja).
""")

st.divider()

# ======================
# Q2: User Segment Analysis
# ======================
st.header("Q2. User Segment Analysis")

# Bar total
fig2, ax2 = plt.subplots()
ax2.bar(["Casual", "Registered"], [total_casual, total_registered])
ax2.set_title("Total Rentals by User Type")
st.pyplot(fig2)

# Line pola jam
hourly_user = hour_df.groupby("hr")[["casual", "registered"]].mean()

fig3, ax3 = plt.subplots()
hourly_user.plot(ax=ax3)
ax3.set_xlabel("Hour")
ax3.set_ylabel("Average Rentals")
ax3.set_title("Hourly Usage Pattern by User Type")
st.pyplot(fig3)

st.write("""
Insight:
- Registered users mendominasi jumlah peminjaman.
- Registered memiliki pola kuat di jam kerja.
- Casual lebih tinggi di siang–sore → leisure usage.
""")

st.divider()

# ======================
# Q3: Weather & Season Impact
# ======================
st.header("Q3. Weather & Season Impact")

# Weather
weather_avg = hour_df.groupby("weathersit")["cnt"].mean()

fig4, ax4 = plt.subplots()
weather_avg.plot(kind="bar", ax=ax4)
ax4.set_title("Average Rentals by Weather Condition")
st.pyplot(fig4)

# Season
season_avg = day_df.groupby("season")["cnt"].mean()

fig5, ax5 = plt.subplots()
season_avg.plot(kind="bar", ax=ax5)
ax5.set_title("Average Rentals by Season")
st.pyplot(fig5)

st.write("""
Insight:
- Cuaca cerah menghasilkan peminjaman tertinggi.
- Musim panas dan gugur lebih ramai dibanding musim dingin.
""")

st.divider()

# ======================
# Clustering (Non-ML)
# ======================
st.header("Demand Clustering (Low - Medium - High)")

hour_cluster = hour_df.groupby("hr")["cnt"].mean().reset_index()
hour_cluster["level"] = pd.qcut(hour_cluster["cnt"], 3, labels=["Low", "Medium", "High"])

fig6, ax6 = plt.subplots()
for level in ["Low", "Medium", "High"]:
    subset = hour_cluster[hour_cluster["level"] == level]
    ax6.scatter(subset["hr"], subset["cnt"], label=level)

ax6.set_xlabel("Hour")
ax6.set_ylabel("Average Rentals")
ax6.legend()
ax6.set_title("Demand Clustering by Hour")
st.pyplot(fig6)

st.write("""
Insight:
- Low demand: dini hari.
- Medium demand: siang.
- High demand: jam sibuk pagi & sore.
""")
