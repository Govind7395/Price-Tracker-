import re
import os
import time
import random
import sqlite3
import logging
from playwright.sync_api import sync_playwright
from .constants import DB_PATH, LOG_DIR
from .price_drop_alert import create_price_alerts_table, check_price_drop
from .db_helper import (
    get_products_to_scrape,
    price_history_table,
    insert_price,
    update_last_scraped,
    mark_scrape_failed,
    mark_scrape_success,
)

LOG_PATH = f"{LOG_DIR}/flipkart.log"

logger = logging.getLogger("flipkart")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_PATH)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def time_delay():
    delay = random.uniform(20, 40)
    logger.info(f"Sleeping for {int(delay)} seconds ")
    time.sleep(delay)


def scrape_flipkart_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        price_text = None

        selectors = ['div[class="hZ3P6w bnqy13"]', 'div[class="hZ3P6w DeU9vF"]']

        try:
            for selector in selectors:
                elements = page.locator(selector)
                if elements.count() > 0:
                    price_text = elements.first.inner_text()
                    break

        except Exception as e:
            logger.exception(f"No selectors found {e}")

        browser.close()

        if not price_text:
            return None

        cleaned = re.sub(r"[^\d.]", "", price_text)
        cleaned = cleaned.split(".")[0]
        return int(cleaned)


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_price_alerts_table(cursor)
    price_history_table(cursor)

    products = get_products_to_scrape(cursor, "flipkart")

    if not products:
        logger.info("No Flipkart Products Found")
        conn.close()
        return

    for product_id, name, url in products:
        logger.info(f"Scraping: {name}")

        try:
            price = scrape_flipkart_product(url)

            if price is None:
                raise ValueError("Price not found")

            insert_price(cursor, product_id, price)
            update_last_scraped(cursor, product_id)
            mark_scrape_success(cursor, product_id)

            drop = check_price_drop(cursor, product_id)

            conn.commit()
            logger.info(f"Saved price: {price}")

            if drop:
                logger.warning(f"PRICE DROP ALERT: {drop}% for product_id={product_id}")

        except Exception as e:
            conn.rollback()
            mark_scrape_failed(cursor, product_id)
            conn.commit()
            logger.exception(f"Error scraping {name}: {e}")

        time_delay()

    conn.close()
    logger.info("All Flipkart products scraped")


# if __name__ == "__main__":
#     main()
