# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st
# from babel.numbers import format_currency
# sns.set(style='dark')

# def create_daily_orders_df(df):
#     daily_orders_df = df.resample(rule='D', on='order_date').agg({
#         "order_id": "nunique",
#         "total_price": "sum"
#     })
#     daily_orders_df = daily_orders_df.reset_index()
#     daily_orders_df.rename(columns={
#         "order_id": "order_count",
#         "total_price": "revenue"
#     }, inplace=True)

#     return daily_orders_df

# def create_sum_order_items_df(df):
#     sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
#     return sum_order_items_df

# def create_bygender_df(df):
#     bygender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
#     bygender_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)

#     return bygender_df

# def create_byage_df(df):
#     byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
#     byage_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)
#     byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])

#     return byage_df

# def create_bystate_df(df):
#     bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
#     bystate_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)

#     return bystate_df


# def create_rfm_df(df):
#     rfm_df = df.groupby(by="customer_id", as_index=False).agg({
#         "order_date": "max", #mengambil tanggal order terakhir
#         "order_id": "nunique",
#         "total_price": "sum"
#     })
#     rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

#     rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
#     recent_date = df["order_date"].dt.date.max()
#     rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
#     rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

#     return rfm_df

# all_df = pd.read_csv("all_data.csv")

# datetime_columns = ["order_date", "delivery_date"]
# all_df.sort_values(by="order_date", inplace=True)
# all_df.reset_index(inplace=True)

# for column in datetime_columns:
#     all_df[column] = pd.to_datetime(all_df[column])


# min_date = all_df["order_date"].min()
# max_date = all_df["order_date"].max()

# with st.sidebar:
#     # Menambahkan logo perusahaan
#     st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

#     # Mengambil start_date & end_date dari date_input
#     start_date, end_date = st.date_input(
#         label='Rentang Waktu',min_value=min_date,
#         max_value=max_date,
#         value=[min_date, max_date]
#     )

# main_df = all_df[(all_df["order_date"] >= str(start_date)) &
#                 (all_df["order_date"] <= str(end_date))]

# daily_orders_df = create_daily_orders_df(main_df)
# sum_order_items_df = create_sum_order_items_df(main_df)
# bygender_df = create_bygender_df(main_df)
# byage_df = create_byage_df(main_df)
# bystate_df = create_bystate_df(main_df)
# rfm_df = create_rfm_df(main_df)

# st.header('Dicoding Collection Dashboard :sparkles:')

# st.subheader('Daily Orders')

# col1, col2 = st.columns(2)

# with col1:
#     total_orders = daily_orders_df.order_count.sum()
#     st.metric("Total orders", value=total_orders)
# with col2:
#     total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO')
#     st.metric("Total Revenue", value=total_revenue)

# fig, ax = plt.subplots(figsize=(16, 8))
# ax.plot(
#     daily_orders_df["order_date"],
#     daily_orders_df["order_count"],
#     marker='o',
#     linewidth=2,
#     color="#90CAF9"
# )
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)

# st.pyplot(fig)

# st.subheader("Best & Worst Performing Product")

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("Number of Sales", fontsize=30)
# ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=35)
# ax[0].tick_params(axis='x', labelsize=30)

# sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
# ax[1].set_ylabel(None)
# ax[1].set_xlabel("Number of Sales", fontsize=30)
# ax[1].invert_xaxis()
# ax[1].yaxis.set_label_position("right")
# ax[1].yaxis.tick_right()
# ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=35)
# ax[1].tick_params(axis='x', labelsize=30)

# st.pyplot(fig)

# st.subheader("Customer Demographics")

# col1, col2 = st.columns(2)

# with col1:
#     fig, ax = plt.subplots(figsize=(20, 10))

#     sns.barplot(
#         y="customer_count",
#         x="gender",
#         data=bygender_df.sort_values(by="customer_count", ascending=False),
#         hue="gender",
#         palette=colors,
#         ax=ax
#     )
#     ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
#     ax.set_ylabel(None)
#     ax.set_xlabel(None)
#     ax.tick_params(axis='x', labelsize=35)
#     ax.tick_params(axis='y', labelsize=30)
#     st.pyplot(fig)

# with col2:
#     fig, ax = plt.subplots(figsize=(20, 10))

#     colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

#     sns.barplot(
#         y="customer_count",
#         x="age_group",
#         data=byage_df.sort_values(by="age_group", ascending=False),
#         palette=colors,
#         hue="age_group",
#         ax=ax
#     )
#     ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
#     ax.set_ylabel(None)
#     ax.set_xlabel(None)
#     ax.tick_params(axis='x', labelsize=35)
#     ax.tick_params(axis='y', labelsize=30)
#     st.pyplot(fig)

# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# sns.barplot(
#     x="customer_count",
#     y="state",
#     data=bystate_df.sort_values(by="customer_count", ascending=False),
#     hue="customer_count",
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by States", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
# st.pyplot(fig)

# st.subheader("Best Customer Based on RFM Parameters")

# col1, col2, col3 = st.columns(3)

# with col1:
#     avg_recency = round(rfm_df.recency.mean(), 1)
#     st.metric("Average Recency (days)", value=avg_recency)

# with col2:
#     avg_frequency = round(rfm_df.frequency.mean(), 2)
#     st.metric("Average Frequency", value=avg_frequency)

# with col3:
#     avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO')
#     st.metric("Average Monetary", value=avg_frequency)

# fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
# colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

# sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("customer_id", fontsize=30)
# ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=30)
# ax[0].tick_params(axis='x', labelsize=35)

# sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
# ax[1].set_ylabel(None)
# ax[1].set_xlabel("customer_id", fontsize=30)
# ax[1].set_title("By Frequency", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=30)
# ax[1].tick_params(axis='x', labelsize=35)

# sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
# ax[2].set_ylabel(None)
# ax[2].set_xlabel("customer_id", fontsize=30)
# ax[2].set_title("By Monetary", loc="center", fontsize=50)
# ax[2].tick_params(axis='y', labelsize=30)
# ax[2].tick_params(axis='x', labelsize=35)

# Batas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    return day, hour

day_df, hour_df = load_data()

# Mapping agar readable
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
hour_df["season_label"] = hour_df["season"].map(season_map)
day_df["season_label"] = day_df["season"].map(season_map)

# =========================
# Title
# =========================
st.title("🚲 Bike Sharing Dashboard")

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("Filter")

# Filter Tahun
year_option = st.sidebar.selectbox("Year", ["All", 2011, 2012])

# Filter Musim
season_option = st.sidebar.multiselect(
    "Season",
    ["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"]
)

# Filter Workingday
day_type = st.sidebar.selectbox("Day Type", ["All", "Working Day", "Weekend / Holiday"])

# =========================
# Apply Filter
# =========================
filtered_hour = hour_df.copy()
filtered_day = day_df.copy()

# Year
if year_option != "All":
    yr_val = 0 if year_option == 2011 else 1
    filtered_hour = filtered_hour[filtered_hour["yr"] == yr_val]
    filtered_day = filtered_day[filtered_day["yr"] == yr_val]

# Season
filtered_hour = filtered_hour[filtered_hour["season_label"].isin(season_option)]
filtered_day = filtered_day[filtered_day["season_label"].isin(season_option)]

# Day type
if day_type == "Working Day":
    filtered_hour = filtered_hour[filtered_hour["workingday"] == 1]
elif day_type == "Weekend / Holiday":
    filtered_hour = filtered_hour[filtered_hour["workingday"] == 0]

# =========================
# Business Overview
# =========================
st.subheader("Business Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", int(filtered_hour["cnt"].sum()))
col2.metric("Casual Users", int(filtered_hour["casual"].sum()))
col3.metric("Registered Users", int(filtered_hour["registered"].sum()))

# =========================
# Q1 Peak Hour
# =========================
st.subheader("Q1: Optimal Operational Time")

hourly_avg = filtered_hour.groupby("hr")["cnt"].mean()

fig1, ax1 = plt.subplots()
hourly_avg.plot(ax=ax1)
ax1.set_xlabel("Hour")
ax1.set_ylabel("Average Rentals")
ax1.set_title("Average Rentals per Hour")
st.pyplot(fig1)

# =========================
# Q2 User Segment
# =========================
st.subheader("Q2: Casual vs Registered")

total_casual = filtered_hour["casual"].sum()
total_registered = filtered_hour["registered"].sum()

fig2, ax2 = plt.subplots()
ax2.bar(["Casual", "Registered"], [total_casual, total_registered])
ax2.set_title("Total Rentals by User Type")
st.pyplot(fig2)

hourly_user = filtered_hour.groupby("hr")[["casual", "registered"]].mean()

fig3, ax3 = plt.subplots()
hourly_user.plot(ax=ax3)
ax3.set_title("Hourly Usage Pattern")
ax3.set_xlabel("Hour")
st.pyplot(fig3)

# =========================
# Q3 Weather & Season
# =========================
st.subheader("Q3: Weather & Season Impact")

weather_avg = filtered_hour.groupby("weathersit")["cnt"].mean()

fig4, ax4 = plt.subplots()
weather_avg.plot(kind="bar", ax=ax4)
ax4.set_title("Average Rentals by Weather")
st.pyplot(fig4)

season_avg = filtered_day.groupby("season_label")["cnt"].mean()

fig5, ax5 = plt.subplots()
season_avg.plot(kind="bar", ax=ax5)
ax5.set_title("Average Rentals by Season")
st.pyplot(fig5)

# =========================
# Clustering Non-ML
# =========================
st.subheader("Demand Clustering (Non-ML)")

hour_cluster = filtered_hour.groupby("hr")["cnt"].mean().reset_index()

hour_cluster["level"] = pd.qcut(
    hour_cluster["cnt"],
    q=3,
    labels=["Low", "Medium", "High"]
)

fig6, ax6 = plt.subplots()
for lvl in ["Low", "Medium", "High"]:
    subset = hour_cluster[hour_cluster["level"] == lvl]
    ax6.scatter(subset["hr"], subset["cnt"], label=lvl)

ax6.legend()
ax6.set_title("Demand Clustering by Hour")
ax6.set_xlabel("Hour")
ax6.set_ylabel("Avg Rentals")
st.pyplot(fig6)
