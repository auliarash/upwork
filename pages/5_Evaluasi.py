import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

MODEL_DIR = ROOT_DIR / "model"
DATA_PATH = ROOT_DIR / "dataset" / "upwork_reviews.csv"

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Evaluasi Model",
    page_icon="📈",
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

st.title("📈 Evaluasi Model Naive Bayes")

st.markdown(
    """
    <div class="custom-card">
        <p>Evaluasi model menggunakan metrik utama, confusion matrix, laporan klasifikasi,
        dan distribusi hasil prediksi untuk memahami performa secara lengkap.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_DIR / "naive_bayes_model.pkl")
    tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
    return model, tfidf

model, tfidf = load_model()

X = tfidf.transform(df["processed_text"].fillna("").astype(str))

y = df["sentiment"]

y_pred = model.predict(X)

accuracy = accuracy_score(y, y_pred)

precision = precision_score(
    y,
    y_pred,
    average="weighted"
)

recall = recall_score(
    y,
    y_pred,
    average="weighted"
)

f1 = f1_score(
    y,
    y_pred,
    average="weighted"
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Accuracy",
    f"{accuracy:.2%}"
)

col2.metric(
    "Precision",
    f"{precision:.2%}"
)

col3.metric(
    "Recall",
    f"{recall:.2%}"
)

col4.metric(
    "F1 Score",
    f"{f1:.2%}"
)

st.markdown("---")

tab_cm, tab_report, tab_dist = st.tabs(["Confusion Matrix", "Classification Report", "Distribusi Prediksi"])

with tab_cm:
    st.subheader("Confusion Matrix")

    cm = confusion_matrix(y,y_pred)

    fig, ax = plt.subplots(figsize=(6,6))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=model.classes_
    )
    disp.plot(ax=ax)

    st.pyplot(fig)

with tab_report:
    st.subheader("Classification Report")

    report = classification_report(
        y,
        y_pred,
        output_dict=True
    )

    report_df = pd.DataFrame(report).transpose()

    st.dataframe(
        report_df,
        use_container_width=True
    )

with tab_dist:
    st.subheader("Distribusi Hasil Prediksi")

    pred = (
        pd.Series(y_pred)
        .value_counts()
        .reset_index()
    )

    pred.columns = [
        "Sentimen",
        "Jumlah"
    ]

    import plotly.express as px

    fig = px.bar(
        pred,
        x="Sentimen",
        y="Jumlah",
        color="Sentimen",
        text="Jumlah"
    )

    st.plotly_chart(fig,use_container_width=True)

