PRICE_DROP_PERCENT = 3


def create_price_alerts_table(cursor):
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS price_alerts(
            id SERIAL PRIMARY KEY,
             product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
              old_price NUMERIC NOT NULL,
               new_price NUMERIC NOT NULL,
                drop_percent NUMERIC NOT NULL,
                 triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
    )


def get_last_two_prices(cursor, product_id):
    cursor.execute(
        """
            SELECT price
            FROM price_history
            WHERE product_id = %s
            ORDER BY scraped_at DESC
            LIMIT 2
            """,
        (product_id,),
    )

    rows = cursor.fetchall()
    return rows if len(rows) == 2 else None


def calculate_price_drop(old_price, new_price):
    if new_price >= old_price:
        return None

    drop = ((old_price - new_price) / old_price) * 100
    return round(drop, 2)


def insert_price_alert(cursor, product_id, old_price, new_price, drop_percent):
    cursor.execute(
        """
            INSERT INTO price_alerts (product_id, old_price, new_price, drop_percent)
            VALUES (%s, %s, %s, %s)
              """,
        (product_id, old_price, new_price, drop_percent),
    )


def check_price_drop(cursor, product_id):
    prices = get_last_two_prices(cursor, product_id)

    if not prices:
        return None

    new_price = prices[0]["price"]
    old_price = prices[1]["price"]

    drop = calculate_price_drop(old_price, new_price)

    if drop and drop >= PRICE_DROP_PERCENT:
        insert_price_alert(cursor, product_id, old_price, new_price, drop)
        return drop

    return None
