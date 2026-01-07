import time
import logging

from constants import LOG_DIR
import amazon, flipkart
from products import create_product_db, get_connection
from db_helper import price_history_table
from price_drop_alert import create_price_alerts_table

logging.basicConfig(
    filename=f"{LOG_DIR}/runner.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("runner")


def main():
    logger.info("Daily scraping started")

    # 🔥 DB bootstrap (RUN ONCE)
    conn = get_connection()
    cursor = conn.cursor()

    create_product_db(cursor)
    price_history_table(cursor)
    create_price_alerts_table(cursor)

    conn.commit()
    cursor.close()
    conn.close()

    # Scrapers
    try:
        amazon.main()
    except Exception:
        logger.exception("Amazon failed")

    time.sleep(10)

    try:
        flipkart.main()
    except Exception:
        logger.exception("Flipkart failed")

    logger.info("Daily scraping finished")


if __name__ == "__main__":
    main()
