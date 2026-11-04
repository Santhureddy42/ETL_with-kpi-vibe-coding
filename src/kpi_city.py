"""Calculate basic customer KPIs for one city."""

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "db" / "analytics.db"


def city_kpi(city: str) -> dict[str, float | int] | None:
    """Print and return customer count, average spend, and churn rate."""
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            """
            SELECT COUNT(*), AVG(monthly_spend), AVG(churned)
            FROM customers_raw
            WHERE city = ?
            """,
            (city,),
        ).fetchone()

    customer_count, average_spend, churn_rate = row
    if customer_count == 0:
        print(f"No customers found for {city!r}.")
        return None

    result: dict[str, float | int] = {
        "customer_count": customer_count,
        "average_monthly_spend": average_spend,
        "churn_rate": churn_rate,
    }
    print(
        f"{city}: {customer_count} customers, "
        f"average monthly spend ${average_spend:.2f}, "
        f"churn rate {churn_rate:.1%}"
    )
    return result


if __name__ == "__main__":
    city_kpi("Mumbai")
    city_kpi("Mumbai' OR 1=1 --")
