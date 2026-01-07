import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

from .constants import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


BASE_DIR = Path(__file__).resolve().parent
SEED_FILES = [
    BASE_DIR / "amazon_products.json",
    BASE_DIR / "flipkart_products.json",
]


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )


def create_product_db(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            last_scraped_at TIMESTAMP,
            last_scrape_status TEXT
        )
        """
    )


def seed_products(cursor, json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        cursor.execute(
            """
            INSERT INTO products (name, platform, url, last_scraped_at)
            VALUES (%s, %s,%s, NULL)
            ON CONFLICT (url) DO NOTHING 
            """,
            (
                product["name"].strip(),
                product["platform"].lower().strip(),
                product["url"].strip(),
            ),
        )


def main():
    print("Inside Main")
    conn = get_connection()
    cursor = conn.cursor()

    create_product_db(cursor)

    for seed_file in SEED_FILES:
        if seed_file.exists():
            seed_products(cursor, seed_file)
        else:
            print(f"Seed file not found: {seed_file}")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
