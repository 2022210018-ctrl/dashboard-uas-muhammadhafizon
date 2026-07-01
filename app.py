import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Dashboard UAS", layout="wide")
st.title("📊 Dashboard Analisis Penjualan Wilayah")
st.markdown("Project UAS: Visualisasi interaktif dengan fitur Hover, Zoom, Maps, dan Drill-Down.")

# Generate Data
@st.cache_data
def generate_data():
    lokasi = [
        {"kota": "Palembang", "lat": -2.9909, "lon": 104.7567},
        {"kota": "Sekayu", "lat": -2.8687, "lon": 103.8115},
        {"kota": "Bengkulu", "lat": -3.7928, "lon": 102.2608},
        {"kota": "Jakarta", "lat": -6.2088, "lon": 106.8456},
        {"kota": "Bandung", "lat": -6.9175, "lon": 107.6191}
    ]
    kategori = ["Elektronik", "Fashion", "Kosmetik", "Perabotan"]
    
    data = []
    for i in range(550):
        kota_pilih = random.choice(lokasi)
        kat_pilih = random.choice(kategori)
        penjualan = random.randint(1000000, 25000000) 
        data.append({
            "ID_Transaksi": f"TRX-{i+1}",
            "Kota": kota_pilih["kota"],
            "Latitude": kota_pilih["lat"],
            "Longitude": kota_pilih["lon"],
            "Kategori": kat_pilih,
            "Total_Penjualan": penjualan,
        })
    return pd.DataFrame(data)

df = generate_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Peta Distribusi Penjualan")
    fig_map = px.scatter_mapbox(
        df, lat="Latitude", lon="Longitude", color="Kategori", size="Total_Penjualan",
        hover_name="Kota", zoom=4.5, mapbox_style="carto-positron"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("2. Komposisi per Kota (Drill-Down)")
    fig_sunburst = px.sunburst(df, path=['Kota', 'Kategori'], values='Total_Penjualan')
    fig_sunburst.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    st.subheader("3. Total Penjualan per Kategori")
    df_bar = df.groupby(["Kota", "Kategori"])["Total_Penjualan"].sum().reset_index()
    fig_bar = px.bar(df_bar, x="Kota", y="Total_Penjualan", color="Kategori", text_auto='.2s')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader(f"Tabel Data Mentah (Total: {len(df)} Records)")
    st.dataframe(df, height=250)