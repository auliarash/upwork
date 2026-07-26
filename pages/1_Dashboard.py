import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

page_style = """
<style>
    .stApp {background: radial-gradient(circle at top left, rgba(56,189,248,0.16), transparent 18%), radial-gradient(circle at bottom right, rgba(192,132,252,0.12), transparent 18%), #020617;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem; color: #e2e8f0; background: transparent;}
    div.stButton > button {border-radius: 999px; border: 1px solid rgba(56,189,248,0.4); background: linear-gradient(135deg,#0ea5e9,#6366f1); color:#f8fafc; box-shadow: 0 16px 40px rgba(14,165,233,0.3);}
    .stMetric {border-radius: 24px; background: rgba(3,37,65,0.95); box-shadow: 0 24px 65px rgba(14,165,233,0.15); border: 1px solid rgba(56,189,248,0.16);}
    .stDataFrame div[style*="overflow-x: auto"] {border-radius: 24px; overflow: hidden; box-shadow: 0 24px 60px rgba(14,165,233,0.12); border: 1px solid rgba(56,189,248,0.16);}
    .stProgress>div>div {background: linear-gradient(135deg,#0ea5e9,#818cf8) !important;}
    .stAlert {background: rgba(15,23,42,0.9) !important; color:#f8fafc !important; border: 1px solid rgba(59,130,246,0.26);}
    .custom-card {background: rgba(3,37,65,0.92); border: 1px solid rgba(59,130,246,0.26); border-radius: 24px; padding: 1.6rem; box-shadow: 0 30px 80px rgba(56,189,248,0.14);}
    .custom-card h2 {color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 0.02em;}
    .custom-card p {color: #cbd5e1; margin: 0;}
    .streamlit-expanderHeader {background: rgba(3,37,65,0.9) !important; color:#38bdf8 !important; border:1px solid rgba(56,189,248,0.25); border-radius:18px !important; padding:0.8rem;}
    .stDataFrame table {border-collapse: separate; border-spacing: 0 0.35rem;}
    .stDataFrame th {background: rgba(8,30,57,0.9); color: #e2e8f0;}
    .stDataFrame td {background: rgba(5,20,44,0.9); color: #e2e8f0;}
    .stTabs button {border-radius: 999px; background: rgba(15,23,42,0.85);}
    .stTabs button[selected] {background: linear-gradient(135deg,#0ea5e9,#6366f1); color:#fff;}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

st.title("📊 Dashboard Analisis Sentimen Upwork")

st.markdown(
    """
    <div class="custom-card">
        <h2>Ringkasan Sentimen Ulasan Upwork</h2>
        <p>Analisis ini menampilkan distribusi sentimen, rating, dan bahasa review untuk membantu
        memahami kualitas layanan dan pengalaman pengguna di Upwork.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================
# Load Dataset
# =====================

df = pd.read_csv("dataset/upwork_reviews.csv")

# =====================
# Statistik
# =====================

total_review = len(df)
positif = (df["sentiment"] == "positif").sum()
negatif = (df["sentiment"] == "negatif").sum()
netral = (df["sentiment"] == "netral").sum()

# =====================
# KPI
# =====================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Review", total_review)
col2.metric("😊 Positif", positif)
col3.metric("😐 Netral", netral)
col4.metric("😞 Negatif", negatif)

import plotly.express as px

sentiment_count = df["sentiment"].value_counts().reset_index()

sentiment_count.columns = ["Sentiment", "Jumlah"]

fig = px.pie(
    sentiment_count,
    names="Sentiment",
    values="Jumlah",
    title="Distribusi Sentimen"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    sentiment_count,
    x="Sentiment",
    y="Jumlah",
    color="Sentiment",
    title="Jumlah Sentimen"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("⭐ Distribusi Rating")

rating = (
    df["rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating.columns = ["Rating", "Jumlah"]

fig = px.bar(
    rating,
    x="Rating",
    y="Jumlah",
    text="Jumlah",
    color="Rating",
    title="Distribusi Rating Pengguna"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🌎 Distribusi Bahasa")

language = (
    df["language"]
    .value_counts()
    .reset_index()
)

language.columns = ["Bahasa", "Jumlah"]

fig = px.bar(
    language,
    x="Bahasa",
    y="Jumlah",
    color="Bahasa",
    title="Distribusi Bahasa Review"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 Informasi Dataset")

col1, col2 = st.columns(2)

with col1:
    st.write("Jumlah Baris")
    st.info(df.shape[0])

    st.write("Jumlah Kolom")
    st.info(df.shape[1])

with col2:
    st.write("Missing Value")
    st.info(df.isnull().sum().sum())

    st.write("Jumlah Bahasa")
    st.info(df["language"].nunique())

st.subheader("📋 Preview Dataset")

show_df = df[
    [
        "review",
        "rating",
        "sentiment",
        "language",
        "date",
        "likes"
    ]
]

st.dataframe(show_df.head(20), use_container_width=True)