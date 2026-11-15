
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "marketpulse.db"

SQL_PATH = BASE_DIR / "sql" / "01_market_analysis.sql"


def run_analysis():

    if not DB_PATH.exists():
        print("Database not found. Run the ETL scripts first.")
        return

    sql_text = SQL_PATH.read_text(encoding="utf-8")

    # Split the SQL file into individual queries
    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    with sqlite3.connect(DB_PATH) as connection:

        for index, query in enumerate(queries, start=1):

            print("\n" + "=" * 55)
            print(f"SQL ANALYSIS {index}")
            print("=" * 55)

            try:
                result = pd.read_sql_query(query, connection)

                if result.empty:
                    print("No matching records found.")
                else:
                    print(result.to_string(index=False))

            except Exception as error:
                print(f"Query {index} failed: {error}")
                raise

    print("\nAll SQL analyses completed successfully!")


if __name__ == "__main__":
    run_analysis()