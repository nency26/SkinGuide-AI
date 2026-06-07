import os
import sqlite3
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import DB_PATH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "datasheet.csv")

def create_database_schema(db_path: str):
    """Initializes the database using the local schema.sql blueprint."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
    conn = sqlite3.connect(db_path)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

def normalize_text(raw_text) -> str:
    """Cleans up messy comma-separated strings."""
    if pd.isna(raw_text) or not isinstance(raw_text, str):
        return ""
    tokens = [token.strip().lower() for token in raw_text.split(",")]
    return ", ".join([t for t in tokens if t])

def run_ingestion():
    """The main ETL pipeline for the CSV file."""
    if not os.path.exists(RAW_DATA_PATH):
        print(f"[ERROR] We couldn't find your CSV at: {RAW_DATA_PATH}")
        return

    print("[ETL] Reading dataset...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    column_mapping = {
        'name': 'product_name', 
        'type': 'product_type',
        'ingridients': 'ingredients', 
        'afterUse': 'tags'
    }
    df = df.rename(columns=column_mapping)
    
    df['product_name'] = df['product_name'].fillna("Unknown").astype(str).str.strip()
    df['brand'] = df['brand'].fillna("Unknown").astype(str).str.strip()
    df['product_type'] = df['product_type'].fillna("Other").astype(str).str.strip()
    df['country'] = df['country'].fillna("Unknown").astype(str).str.strip()
    
    df['ingredients'] = df['ingredients'].apply(normalize_text)
    df['tags'] = df['tags'].apply(normalize_text)
    
    df = df[df['ingredients'] != ""]
    final_df = df[['product_name', 'brand', 'product_type', 'country', 'ingredients', 'tags']]
    
    conn = sqlite3.connect(DB_PATH)
    final_df.to_sql('products', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"[ETL] Success! {len(final_df)} clean products loaded into the database.")

if __name__ == "__main__":
    create_database_schema(DB_PATH)
    run_ingestion()