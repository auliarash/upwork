import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

DATA_PATH = ROOT_DIR / "dataset" / "upwork_reviews.csv"

st.set_page_config(
    page_title="Visualisasi",
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

st.title("📊 Visualisasi Data")

st.markdown(
    """
    <div class="custom-card">
        <p>Temukan insight visual dari distribusi sentimen, rating, bahasa, dan kata kunci paling populer
        di ulasan Upwork.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# Load Dataset
# ==========================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def build_text(series):
    return " ".join(
        str(value) if pd.notna(value) else ""
        for value in series
    )


df = load_data()

# ==========================
# Filter
# ==========================

st.sidebar.header("Filter")

sentiment_filter = st.sidebar.multiselect(
    "Sentiment",
    df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

df = df[df["sentiment"].isin(sentiment_filter)]

st.subheader("🥧 Distribusi Sentimen")

sentiment = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment.columns = ["Sentiment", "Jumlah"]

fig = px.pie(
    sentiment,
    names="Sentiment",
    values="Jumlah",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Jumlah Sentimen")

fig = px.bar(
    sentiment,
    x="Sentiment",
    y="Jumlah",
    color="Sentiment",
    text="Jumlah"
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
    color="Rating",
    text="Jumlah"
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
    text="Jumlah"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("☁️ WordCloud Sentimen Positif")

positive_text = build_text(
    df[df["sentiment"] == "positif"]["processed_text"]
)

wc = WordCloud(
    width=900,
    height=400,
    background_color="white"
).generate(positive_text)

fig, ax = plt.subplots(figsize=(12,5))
ax.imshow(wc)
ax.axis("off")

st.pyplot(fig)

st.subheader("☁️ WordCloud Sentimen Negatif")

negative_text = build_text(
    df[df["sentiment"] == "negatif"]["processed_text"]
)

wc = WordCloud(
    width=900,
    height=400,
    background_color="white"
).generate(negative_text)

fig, ax = plt.subplots(figsize=(12,5))
ax.imshow(wc)
ax.axis("off")

st.pyplot(fig)

st.subheader("🔥 Top 20 Kata")

text = build_text(df["processed_text"])

counter = Counter(text.split())

top20 = pd.DataFrame(
    counter.most_common(20),
    columns=["Kata","Frekuensi"]
)

fig = px.bar(
    top20,
    x="Frekuensi",
    y="Kata",
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)