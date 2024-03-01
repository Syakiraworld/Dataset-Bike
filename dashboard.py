import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
colors = sns.color_palette("pastel") 

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.header('Sepeda analisis:sparkles:')
    st.image("bike.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

st.header('Dicoding Collection Dashboard :sparkles:')
st.subheader('Q1: Bagiamana pengaruh cuaca terhadap jumlah sewa harian?')
weathersit_info="""
1: Clear, Few clouds, Partly cloudy, Partly cloudy |
2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist |
3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
"""

st.markdown(f"**weathersit:**\n{weathersit_info}")
byweat_df = all_df.groupby(by="weathersit_day").registered_hour.nunique().reset_index()
byweat_df.rename(columns={"registered_hour": "registered_hour_count"}, inplace=True)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="registered_hour_count",
    x="weathersit_day",
    data=byweat_df.sort_values(by="registered_hour_count", ascending=False),
    palette=colors,
    ax=ax
)
plt.title("Number of Customer registered by weather", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader('Q2 : Bagimana kondisi penyewa registered di tiap bulan?')



mnth_day_all_df = all_df.resample(rule='M', on='dteday').agg({
    "cnt_hour": "nunique",
})
mnth_day_all_df.index = mnth_day_all_df.index.strftime('%B') #mengubah format order date menjadi Tahun-Bulan
mnth_day_all_df = mnth_day_all_df.reset_index()
mnth_day_all_df.rename(columns={
    "cnt_day": "nunique",
}, inplace=True)
mnth_day_all_df.head(12)

fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(
    mnth_day_all_df["dteday"],
    mnth_day_all_df["cnt_hour"],
    marker='o',
    linewidth=1,
    color="#72BCD4"
)
plt.title("Kondisi penyewa setiap bulan 2011 dan 2012", loc="center", fontsize=18)
plt.xticks(fontsize=10, rotation=45)  # Add tick locations or labels if needed
plt.yticks(fontsize=10)
st.pyplot(fig)
