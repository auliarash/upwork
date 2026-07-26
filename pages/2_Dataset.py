import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dataset",
    page_icon="📂",
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

st.title("📂 Dataset Ulasan Upwork")

st.markdown(
    """
    <div class="custom-card">
        <p>Telusuri dataset ulasan Upwork, filter menurut sentimen, bahasa, dan rating,
        lalu unduh hasil yang sudah disesuaikan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===========================
# Load Dataset
# ===========================

@st.cache_data
def load_data():
    return pd.read_csv("dataset/upwork_reviews.csv")

df = load_data()

# ===========================
# Sidebar Filter
# ===========================

st.sidebar.header("Filter Dataset")

# Filter Sentimen
sentiment = st.sidebar.multiselect(
    "Pilih Sentimen",
    options=df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

# Filter Bahasa
language = st.sidebar.multiselect(
    "Pilih Bahasa",
    options=sorted(df["language"].dropna().unique()),
    default=sorted(df["language"].dropna().unique())
)

# Filter Rating
rating = st.sidebar.multiselect(
    "Pilih Rating",
    options=sorted(df["rating"].unique()),
    default=sorted(df["rating"].unique())
)

# ===========================
# Search Review
# ===========================

keyword = st.text_input(
    "🔍 Cari Review",
    placeholder="Masukkan kata kunci..."
)

# ===========================
# Filter Data
# ===========================

filtered_df = df[
    (df["sentiment"].isin(sentiment)) &
    (df["language"].isin(language)) &
    (df["rating"].isin(rating))
]

if keyword:
    filtered_df = filtered_df[
        filtered_df["review"]
        .str.contains(keyword, case=False, na=False)
    ]

# ===========================
# Statistik
# ===========================

st.write(f"### Jumlah Data : {len(filtered_df)} Review")

# ===========================
# Pilih Kolom
# ===========================

columns = st.multiselect(
    "Pilih Kolom yang Ditampilkan",
    options=df.columns.tolist(),
    default=[
        "username",
        "review",
        "rating",
        "sentiment",
        "language",
        "date",
        "likes"
    ]
)

show_preprocessing = st.checkbox(
    "Tampilkan Kolom Preprocessing",
    value=False
)

if show_preprocessing:
    columns = columns + [
        "case_folding",
        "cleaning",
        "token",
        "stopword",
        "stemming",
        "processed_text"
    ]

# Menghindari kolom ganda
columns = list(dict.fromkeys(columns))

st.dataframe(
    filtered_df[columns],
    use_container_width=True,
    hide_index=True
)

# ===========================
# Download Dataset
# ===========================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="filtered_upwork_reviews.csv",
    mime="text/csv"
)