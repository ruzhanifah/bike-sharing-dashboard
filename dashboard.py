import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Data
df = pd.read_csv(r'E:\Coding Camp 2026\Proyek Analisis Data\Dashboard\day.csv')

df['dteday'] = pd.to_datetime(df['dteday'])
df['month'] = df['dteday'].dt.month
df['day_name'] = df['dteday'].dt.day_name()

# Mapping
df['season'] = df['season'].replace({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

df['weathersit'] = df['weathersit'].replace({
    1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'
})

# Title
st.title("Bike Sharing Dashboard 🚲")
st.markdown("Analisis pengaruh cuaca, musim, dan pola waktu terhadap penyewaan sepeda.")

# Sidebar Filter
st.sidebar.header("Filter Data")

season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season'].unique(),
    default=df['season'].unique()
)

month_filter = st.sidebar.slider(
    "Pilih Rentang Bulan",
    1, 12, (1, 12)
)

# Filter data
df_filtered = df[
    (df['season'].isin(season_filter)) &
    (df['month'] >= month_filter[0]) &
    (df['month'] <= month_filter[1])
]

# METRICS
st.subheader("Ringkasan Data 📊")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(df_filtered['cnt'].sum()))
col2.metric("Rata-rata Harian", int(df_filtered['cnt'].mean()))
col3.metric("Penyewaan Maksimum", int(df_filtered['cnt'].max()))

# Visual 1: Musim
st.subheader("Pengaruh Musim terhadap Penyewaan 🌿")

fig, ax = plt.subplots()
sns.barplot(x='season', y='cnt', data=df_filtered, estimator='mean', ax=ax)
st.pyplot(fig)

# Visual 2: Cuaca
st.subheader("Pengaruh Cuaca terhadap Penyewaan 🌤️")

fig, ax = plt.subplots()
sns.barplot(x='weathersit', y='cnt', data=df_filtered, estimator='mean', ax=ax)
plt.xticks(rotation=30)
st.pyplot(fig)

# Visual 3: User Type
st.subheader("Registered vs Casual per Bulan 👥")

fig, ax = plt.subplots()
sns.lineplot(x='month', y='registered', data=df_filtered, ax=ax, label='Registered')
sns.lineplot(x='month', y='casual', data=df_filtered, ax=ax, label='Casual')
st.pyplot(fig)

# Visual 4: Hari
st.subheader("Pola Penyewaan per Hari 📅")

fig, ax = plt.subplots()
sns.barplot(
    x='day_name',
    y='cnt',
    data=df_filtered,
    order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
    ax=ax
)
plt.xticks(rotation=45)
st.pyplot(fig)

# Insight
st.subheader("Insight Utama 📌")

st.markdown("""
### Pengaruh Cuaca & Musim 🔍
- Penyewaan tertinggi terjadi pada musim dengan kondisi cuaca yang nyaman.
- Cuaca cerah menghasilkan jumlah penyewaan paling tinggi.
- Cuaca buruk seperti hujan menurunkan jumlah penyewaan.

### Pola Waktu & Pengguna 📅
- Permintaan meningkat pada bulan-bulan tertentu (seasonal).
- Penyewaan cenderung lebih tinggi pada akhir pekan.
- Pengguna registered lebih dominan dibandingkan casual.

### Rekomendasi Bisnis 🚀
- Fokus promosi pada musim dan cuaca yang mendukung.
- Maksimalkan operasional saat peak season.
- Tingkatkan pengguna casual dengan promo weekend & diskon pengguna baru.  
""")

# Analisis Lanjutan
st.subheader("Analisis Lanjutan: Pola Penyewaan per Jam ⏰")

# Load hour dataset
df_hour = pd.read_csv(r'E:\Coding Camp 2026\Proyek Analisis Data\Dashboard\hour.csv')

# Preprocessing
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Rata-rata penyewaan per jam
hourly = df_hour.groupby('hr')['cnt'].mean()

# Visualisasi
fig, ax = plt.subplots()
sns.lineplot(x=hourly.index, y=hourly.values, ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Pola Penyewaan Sepeda per Jam")
st.pyplot(fig)

# Heatmap
st.subheader("Heatmap Penyewaan (Jam vs Hari) 🔥")

heatmap_data = df_hour.groupby(['weekday','hr'])['cnt'].mean().unstack()

fig, ax = plt.subplots()
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Hari (0=Min, 6=Sabtu)")
st.pyplot(fig)

# Insight
st.subheader("Insight dari Data Jam 📌")

st.markdown("""
### Pola Jam Sibuk
- Terdapat dua puncak utama:
  - Pagi (sekitar 07.00–09.00)
  - Sore (sekitar 17.00–19.00)

### Interpretasi
- Pola ini menunjukkan penggunaan sepeda untuk aktivitas commuting (berangkat & pulang kerja/sekolah).

### Rekomendasi Bisnis
- Tambahkan ketersediaan sepeda di jam sibuk.
- Berikan promo di jam sepi untuk meningkatkan utilisasi.
- Targetkan pengguna casual di luar jam commuting.
""")