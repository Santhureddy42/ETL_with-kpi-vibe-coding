"""Load the raw customer CSV into the project's SQLite database."""

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "customers_raw.csv"
DB_PATH = PROJECT_ROOT / "data" / "db" / "analytics.db"


def load_customers() -> int:
    """Replace the customers_raw table with the rows in the source CSV."""
    customers = pd.read_csv(
        CSV_PATH,
        dtype={
            "customer_id": "int64",
            "city": "string",
            "monthly_spend": "float64",
            "churned": "int64",
        },
    )
    expected_columns = [
        "customer_id",
        "city",
        "monthly_spend",
        "churned",
    ]
    missing_columns = set(expected_columns) - set(customers.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {sorted(missing_columns)}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("DROP TABLE IF EXISTS customers_raw")
        connection.execute(
            """
            CREATE TABLE customers_raw (
                customer_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                monthly_spend REAL NOT NULL,
                churned INTEGER NOT NULL CHECK (churned IN (0, 1))
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO customers_raw
                (customer_id, city, monthly_spend, churned)
            VALUES (?, ?, ?, ?)
            """,
            customers[expected_columns].itertuples(index=False, name=None),
        )

    return len(customers)


if __name__ == "__main__":
    row_count = load_customers()
    print(f"Loaded {row_count} customers into {DB_PATH}")
