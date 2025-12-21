import sqlite3


PRICE_DROP_PERCENT = 3


def create_price_alerts_table(cursor):
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS price_alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
             product_id INTEGER NOT NULL,
              old_price INTEGER NOT NULL,
               new_price INTEGER NOT NULL,
                drop_percent REAL NOT NULL,
                 triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """
    )


def get_last_two_prices(cursor, product_id):
    cursor.execute(
        """
            SELECT price
            FROM price_history
            WHERE product_id = ?
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
            VALUES (?, ?, ?, ?)
              """,
        (product_id, old_price, new_price, drop_percent),
    )


def check_price_drop(cursor, product_id):
    prices = get_last_two_prices(cursor, product_id)

    if not prices:
        return None

    new_price = prices[0][0]
    old_price = prices[1][0]

    drop = calculate_price_drop(old_price, new_price)

    if drop and drop >= PRICE_DROP_PERCENT:
        insert_price_alert(cursor, product_id, old_price, new_price, drop)
        return drop

    return None
