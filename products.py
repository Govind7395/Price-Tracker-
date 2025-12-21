import os
import json
import sqlite3
from pathlib import Path
from .constants import DB_PATH


SEED_FILES = ["amazon_products.json", "flipkart_products.json"]


def create_product_db(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            INSERT OR IGNORE INTO products (name, platform, url, last_scraped_at)
            VALUES (?, ?,?, NULL)
            """,
            (
                product["name"].strip(),
                product["platform"].lower().strip(),
                product["url"].strip(),
            ),
        )


def main():
    print("Inside Main")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_product_db(cursor)

    for seed_file in SEED_FILES:
        if Path(seed_file).exists():
            seed_products(cursor, seed_file)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
