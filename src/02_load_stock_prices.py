
import sqlite3
from pathlib import Path

import pandas as pd
import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "marketpulse.db"

# Public stock symbols for portfolio demonstration
STOCKS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "JPM": "JPMorgan Chase"
}


def load_stock_prices():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Database not found. Run "
            "src/01_create_database.py first."
        )

    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        for ticker, company_name in STOCKS.items():

            print(f"\nDownloading {ticker}...")

            # Retrieve one year of historical data
            stock = yf.Ticker(ticker)

            data = stock.history(
                period="1y",
                auto_adjust=True
            )

            if data.empty:
                print(f"No data found for {ticker}.")
                continue

            # Keep required fields
            data = data[["Close", "Volume"]].copy()
            data = data.dropna(subset=["Close"])

            # Calculate daily percentage returns as decimals
            data["daily_return"] = (
                data["Close"].pct_change()
            )

            # Convert date index to ISO date strings
            data["date"] = data.index.strftime("%Y-%m-%d")

            # Add/update stock information
            connection.execute("""
                INSERT INTO stocks (ticker, company_name)
                VALUES (?, ?)
                ON CONFLICT(ticker)
                DO UPDATE SET
                    company_name = excluded.company_name
            """, (ticker, company_name))

            stock_id = connection.execute("""
                SELECT stock_id
                FROM stocks
                WHERE ticker = ?
            """, (ticker,)).fetchone()[0]

            # Prepare historical price records
            records = []

            for _, row in data.iterrows():

                daily_return = (
                    None
                    if pd.isna(row["daily_return"])
                    else float(row["daily_return"])
                )

                records.append((
                    stock_id,
                    row["date"],
                    float(row["Close"]),
                    int(row["Volume"]),
                    daily_return
                ))

            # Insert records without duplicating dates
            connection.executemany("""
                INSERT INTO stock_prices (
                    stock_id,
                    date,
                    close_price,
                    volume,
                    daily_return
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(stock_id, date)
                DO UPDATE SET
                    close_price = excluded.close_price,
                    volume = excluded.volume,
                    daily_return = excluded.daily_return
            """, records)

            connection.commit()

            print(
                f"{ticker}: {len(records)} "
                "daily records processed."
            )

    finally:
        connection.close()

    print("\nStock price ETL completed!")


if __name__ == "__main__":
    load_stock_prices()