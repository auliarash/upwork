import pandas as pd
import re
import string
import nltk
from langdetect import detect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Ensure NLTK data is downloaded (only runs once if not already downloaded)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True) # Ensure punkt_tab is downloaded if used previously

def detect_lang(text):
    try:
        return detect(str(text))
    except:
        return 'unknown'

def cleaning(text):
    if pd.isna(text):
        text = ""
    else:
        text = str(text)

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

# Initialize stemmers and stopwords outside functions for efficiency
factory = StemmerFactory()
stemmer_id = factory.create_stemmer()
stemmer_en = PorterStemmer()

stop_id = set(stopwords.words('indonesian'))
stop_en = set(stopwords.words('english'))

def remove_stopwords(tokens, lang):
    if lang == 'id':
        return [word for word in tokens if word not in stop_id]
    elif lang == 'en':
        return [word for word in tokens if word not in stop_en]
    else:
        return tokens

def stemming(tokens, lang):
    hasil=[]
    if lang=='id':
        for word in tokens:
            hasil.append(stemmer_id.stem(word))
    elif lang=='en':
        for word in tokens:
            hasil.append(stemmer_en.stem(word))
    else:
        hasil=tokens
    return hasil

def preprocess_text(text):
    """Applies all preprocessing steps to a given text."""
    # 1. Detect language
    lang = detect_lang(text)

    # 2. Case folding and cleaning
    cleaned_text = cleaning(text.lower())

    # 3. Tokenization
    tokens = word_tokenize(cleaned_text)

    # 4. Stopword removal
    tokens_no_stopwords = remove_stopwords(tokens, lang)

    # 5. Stemming
    stemmed_tokens = stemming(tokens_no_stopwords, lang)

    # 6. Join back to string
    return ' '.join(stemmed_tokens)

print("preprocessing.py created successfully!")
