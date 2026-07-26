import streamlit as st
import joblib
import pandas as pd

from utils.preprocessing import preprocess_text

# ===========================
# Konfigurasi
# ===========================

st.set_page_config(
    page_title="Prediksi Sentimen",
    page_icon="🤖",
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

st.title("🤖 Prediksi Sentimen Review Upwork")

st.markdown(
    """
    <div class="custom-card">
        <p>Masukkan review, lalu model akan menampilkan preprocessing, prediksi sentimen,
        dan confidence score dalam format yang lebih mudah dibaca.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Masukkan sebuah review, kemudian sistem akan melakukan preprocessing "
    "dan memprediksi sentimennya menggunakan model Multinomial Naive Bayes."
)

# ===========================
# Load Model
# ===========================

@st.cache_resource
def load_model():
    model = joblib.load("model/naive_bayes_model.pkl")
    tfidf = joblib.load("model/tfidf_vectorizer.pkl")
    return model, tfidf

model, tfidf = load_model()

# ===========================
# Input Review
# ===========================

review = st.text_area(
    "Masukkan Review",
    height=180,
    placeholder="Contoh: This application is very useful for freelancers..."
)

if st.button("Prediksi Sentimen"):

    if review.strip() == "":
        st.warning("Silakan masukkan review terlebih dahulu.")

    processed = preprocess_text(review)

    st.subheader("Hasil Preprocessing")

    st.code(processed)
    
    vector = tfidf.transform([processed])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    st.subheader("Hasil Prediksi")

    if prediction == "positif":
        st.success("😊 Sentimen Positif")

    elif prediction == "negatif":
        st.error("😞 Sentimen Negatif")

    else:
        st.info("😐 Sentimen Netral")

    st.subheader("Probabilitas")

    prob = pd.DataFrame({
        "Sentimen": model.classes_,
        "Probabilitas": probability
    })

    st.dataframe(
        prob.style.format({"Probabilitas":"{:.2%}"}),
        use_container_width=True
    )

    st.subheader("Confidence Score")

    for sentiment, score in zip(model.classes_, probability):

        st.write(sentiment)

        st.progress(float(score))