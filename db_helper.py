def price_history_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            price INTEGER NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              )
        """
    )


def insert_price(cursor, product_id, price):
    cursor.execute(
        """
        INSERT INTO price_history (product_id, price)
        VALUES (%s, %s)
        """,
        (product_id, price),
    )


def mark_scrape_success(cursor, product_id):
    cursor.execute(
        """
        UPDATE products
        SET last_scrape_status = 'success',
            last_scraped_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (product_id,),
    )


def mark_scrape_failed(cursor, product_id):
    cursor.execute(
        """
        UPDATE products
        SET last_scrape_status = 'failed'
        WHERE id = %s
        """,
        (product_id,),
    )


def update_last_scraped(cursor, product_id):
    cursor.execute(
        """
            UPDATE products 
            SET last_scraped_at = CURRENT_TIMESTAMP
            WHERE  id = %s
        """,
        (product_id,),
    )


def get_products_to_scrape(cursor, platform):
    cursor.execute(
        """
        SELECT id, name, url
        FROM products
        WHERE platform = %s
        AND (
            last_scraped_at IS NULL
            OR last_scrape_status = 'failed'
            OR last_scraped_at::date < CURRENT_DATE
            )
        ORDER BY id
        """,
        (platform,),
    )

    product = cursor.fetchall()
    return product
