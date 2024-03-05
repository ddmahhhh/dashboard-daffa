import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='ticks')
from datetime import datetime
import datetime as dt

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title='Air Quality', page_icon=':bar_chart:', layout='wide')

# Header
st.title('Air Quality Dashboard')
st.subheader('Daffa Maheswara Iswidono')

# Memuat data
df = pd.read_csv("merged.csv")

# Tambahkan kolom "date" dengan menggabungkan kolom 'year', 'month', dan 'day'
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style='display: flex; align-items: center; justify-content: center;'>
            <div style='margin-left: 10px; font-size: 24px; font-weight: bold; color: #FFFFFF;'>Daffa Air Quality Projects</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<hr style='margin: 12px 0; border-color: #FF0000;'>", unsafe_allow_html=True)

    st.markdown("[Air Quality dataset](merged.csv)")

    st.markdown("<hr style='margin: 12px 0; border-color: #FF0000;'>", unsafe_allow_html=True)

    st.markdown("### Contact")
    st.markdown(
        """
        Email: [M004D4KY3025@bangkit.academy](mailto:M004D4KY3025@bangkit.academy)
        """,
        unsafe_allow_html=True
    )

# Dropdown untuk memilih kota
selected_city = st.selectbox("Pilih Kota", df['station'].unique())

# Slider untuk memilih rentang tahun
selected_years = st.slider("Pilih Rentang Tahun", min_value=min(df['year']), max_value=max(df['year']), value=(min(df['year']), max(df['year'])))

# Filter data berdasarkan kota dan rentang tahun yang dipilih
filtered_data = df[(df['station'] == selected_city) & (df['year'].between(selected_years[0], selected_years[1]))]

# Tren kualitas udara dalam periode yang dipilih
st.header("Tren Kualitas Udara")
daily_data = filtered_data.groupby('date').agg({'PM2.5': 'mean', 'PM10': 'mean', 'SO2': 'mean', 'NO2': 'mean', 'CO': 'mean', 'O3': 'mean'})
fig, ax = plt.subplots(figsize=(12, 6))
for column in daily_data.columns:
    ax.plot(daily_data.index, daily_data[column], label=column)

ax.set_title('Variasi Harian Kualitas Udara')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Nilai Rata-Rata')
ax.legend()
st.pyplot(fig)

# Bar chart untuk menampilkan banyaknya polutan
st.header("Banyaknya Polutan")
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
mean_pollutants = filtered_data.groupby('month')[pollutants].mean().reset_index()
mean_pollutants = pd.melt(mean_pollutants, id_vars=['month'], value_vars=pollutants, var_name='Pollutant', value_name='Mean Concentration')
fig = plt.figure(figsize=(12, 6))
sns.barplot(data=mean_pollutants, x='month', y='Mean Concentration', hue='Pollutant')
plt.title('Rata-rata Konsentrasi Polutan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Konsentrasi')
plt.legend(title='Polutan')
st.pyplot(fig)
