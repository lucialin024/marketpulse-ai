
import sqlite3
from pathlib import Path

# Locate the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Define database location
DB_PATH = BASE_DIR / "data" / "marketpulse.db"

# Ensure the data folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_database():
    connection = sqlite3.connect(DB_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    cursor = connection.cursor()

    # Table 1: Stock information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL UNIQUE,
            company_name TEXT NOT NULL
        )
    """)

    # Table 2: Historical stock prices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            close_price REAL NOT NULL,
            volume INTEGER,
            daily_return REAL,

            FOREIGN KEY (stock_id)
                REFERENCES stocks(stock_id),

            UNIQUE(stock_id, date)
        )
    """)

    connection.commit()
    connection.close()

    print("MarketPulse AI database created successfully!")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    create_database()