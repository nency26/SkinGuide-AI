import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

from database.connection import fetch_all_products

ARTIFACT_DIR = r"E:\SkinGuide\recommendation_models\pickled_models"
VECTORIZER_PATH = os.path.join(ARTIFACT_DIR, "vectorizer.pkl")
MATRIX_PATH = os.path.join(ARTIFACT_DIR, "product_matrix.pkl")

def custom_ingredient_tokenizer(text: str):
    """Safely splits ingredient strings by comma for the vectorizer."""
    if not isinstance(text, str):
        return []
    return [i.strip() for i in text.split(',') if i.strip()]

def train_and_save_model():
    """Trains the vocabulary matrix on the internal database and saves models using Pickle."""
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    products = fetch_all_products()
    
    if not products:
        print("[ERROR] Database is empty. Please run your ingestion script first.")
        return
        
    df = pd.DataFrame(products)
    print(f"[ML Engine] Tokenizing and fitting matrix vectorizer on {len(df)} items...")
    
    vectorizer = TfidfVectorizer(
        tokenizer=custom_ingredient_tokenizer,
        token_pattern=None
    )
    
    product_matrix = vectorizer.fit_transform(df['ingredients'])
    
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(MATRIX_PATH, 'wb') as f:
        pickle.dump(product_matrix, f)
        
    print(f"[ML Engine] Pickled structures compiled and stored successfully in {ARTIFACT_DIR}")

def load_artifacts():
    """Utility for the backend to extract pickled binaries into memory."""
    if not os.path.exists(VECTORIZER_PATH) or not os.path.exists(MATRIX_PATH):
        raise FileNotFoundError("Compiled ML artifacts are missing. Run vectorizer.py directly first.")
        
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(MATRIX_PATH, 'rb') as f:
        product_matrix = pickle.load(f)
        
    return vectorizer, product_matrix

if __name__ == "__main__":
    train_and_save_model()