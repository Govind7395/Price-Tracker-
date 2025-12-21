import os

BASE_DIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASE_DIR, "price_alert.db")

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
