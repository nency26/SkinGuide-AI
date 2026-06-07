import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "skincare.db")

@contextmanager
def get_db_connection():
    """Context manager for safe database connections."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  
        yield conn
    except sqlite3.Error as e:
        print(f"[DB ERROR] Database connection failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def fetch_all_products():
    """Retrieves the entire product catalog for the ML engine."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return [dict(row) for row in cursor.fetchall()]