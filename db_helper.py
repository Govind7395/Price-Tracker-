def price_history_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price INTEGER NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) 
              )
        """
    )


def insert_price(cursor, product_id, price):
    cursor.execute(
        """
        INSERT INTO price_history (product_id, price)
        VALUES (?, ?)
        """,
        (product_id, price),
    )


def mark_scrape_success(cursor, product_id):
    cursor.execute(
        """
        UPDATE products
        SET last_scrape_status = 'success',
            last_scraped_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (product_id,),
    )


def mark_scrape_failed(cursor, product_id):
    cursor.execute(
        """
        UPDATE products
        SET last_scrape_status = 'failed'
        WHERE id = ?
        """,
        (product_id,),
    )


def update_last_scraped(cursor, product_id):
    cursor.execute(
        """
            UPDATE products 
            SET last_scraped_at = CURRENT_TIMESTAMP
            WHERE  id = ?
        """,
        (product_id,),
    )


def get_products_to_scrape(cursor, platform):
    cursor.execute(
        """
        SELECT id, name, url
        FROM products
        WHERE platform = ?
        AND (
            last_scraped_at IS NULL
            OR last_scrape_status = 'failed'
            OR DATE(last_scraped_at) < DATE('now')
            )
        ORDER BY id
        """,
        (platform,),
    )

    product = cursor.fetchall()
    return product
