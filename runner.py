import time
import logging
from .constants import LOG_DIR
from . import amazon, flipkart

logging.basicConfig(
    filename=f"{LOG_DIR}/runner.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("runner")


def main():
    logger.info("Daily scraping started")

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
