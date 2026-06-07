CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    brand TEXT NOT NULL,
    product_type TEXT NOT NULL,
    country TEXT,
    ingredients TEXT NOT NULL,
    tags TEXT
);

CREATE INDEX IF NOT EXISTS idx_product_type ON products (product_type);