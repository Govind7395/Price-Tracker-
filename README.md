# Price Tracker 

A Python-based price tracking system that monitors product prices on **Amazon** and **Flipkart**, stores historical data in SQLite, and triggers price-drop alerts.

Built with **Playwright** for scraping and **SQLite** for persistence.

---

## Features

- Scrapes prices from Amazon & Flipkart
- Stores full price history in SQLite
- Detects percentage-based price drops
- Structured logging (per site + runner)
- Can be automated using Windows Task Scheduler

---

## Project Structure

```text
Price_Tracker/
│
├── amazon.py              # Amazon scraper
├── flipkart.py            # Flipkart scraper
├── runner.py              # Entry point (runs all scrapers)
├── products.py            # Product definitions
├── db_helper.py           # Database helpers
├── price_drop_alert.py    # Price drop detection logic
├── constants.py           # Paths & constants
│
├── logs/                  # Runtime logs (ignored in git)
├── requirements.txt       # Python dependencies
├── README.md
└── __init__.py


---

##  Setup Instructions

### Clone the repository
```bash
git clone https://github.com/Govind7395/Price-Tracker.git
cd Price-Tracker
```


---

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
```

---

## To Run the Project

```bash
python -m Price_Tracker.runner
```

---

## Logging
- Logs are stored per module

```text
logs/
├── amazon.log
├── flipkart.log
└── runner.log
```
- Each log contains timestamps, severity levels, and detailed error traces


---

## Database
- Uses SQLite
- Automatically creates required tables
- Tracks:
   - Products
   - Price history
   - Last scrape status
   - Price drop alerts
- Database files are excluded from Git

---

## Automation
- This project is compatible with Windows Task Scheduler
- You can configure it to:
   - Run daily
   - Run on startup
   - Run headless in background

---

## Notes

- Scraping depends on site structure and selectors may change over time.
- This project is intended for learning and personal automation use.


