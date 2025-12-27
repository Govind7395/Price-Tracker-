import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load .env relative to the package
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# Paths
DB_PATH = os.path.join(BASE_DIR, "price_alert.db")

# Keys
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
USER_API_KEY = os.getenv("USER_API_KEY")

if not ADMIN_API_KEY or not USER_API_KEY:
    raise RuntimeError("API keys not set in environment")

# Logs
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
