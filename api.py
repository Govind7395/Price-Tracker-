from fastapi import FastAPI, Request
from fastapi import Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

from .constants import ADMIN_API_KEY, USER_API_KEY
from .products import get_connection

BASE_DIR = Path(__file__).resolve().parent
# templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(title="Price Tracker API")


def verify_user_key(x_api_key: str = Header(...)):
    if x_api_key not in {USER_API_KEY, ADMIN_API_KEY}:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key


def verify_admin_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Admin Access only")
    return x_api_key


@app.get("/api/products")
def get_products(api_key: str = Depends(verify_user_key)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            p.id,
            p.name,
            p.platform,
            ph.price AS last_price
        FROM products p
        LEFT JOIN price_history ph
            ON ph.product_id = p.id
            AND ph.scraped_at = (
                SELECT MAX(scraped_at)
                FROM price_history
                WHERE product_id = p.id
            )
        ORDER BY p.id
    """
    )

    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return products


@app.post("/api/admin/products")
def add_product(
    name: str, platform: str, url: str, api_key: str = Depends(verify_admin_key)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO  products (name, platform, url) VALUES (%s, %s, %s)
        ON CONFLICT (url) DO NOTHING
        """,
        (name, platform, url),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "product added"}
