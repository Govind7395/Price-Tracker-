import os
from dotenv import load_dotenv
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load .env
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# Cloud Database
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port
    DB_NAME = parsed.path.lstrip("/")
    DB_USER = parsed.username
    DB_PASSWORD = parsed.password

# Local .env
else:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

# if not all([DB_NAME, DB_USER, DB_PASSWORD]):
# raise RuntimeError("PostgreSQL DB credentials not set in environment")

# Keys
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
USER_API_KEY = os.getenv("USER_API_KEY")

# if not ADMIN_API_KEY or not USER_API_KEY:
# raise RuntimeError("API keys not set in environment")

# Logs
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
