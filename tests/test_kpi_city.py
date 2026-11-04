import sqlite3

import pytest

from src import kpi_city


@pytest.fixture
def sample_database(tmp_path, monkeypatch):
    database_path = tmp_path / "analytics.db"
    monkeypatch.setattr(kpi_city, "DB_PATH", database_path)

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE customers_raw (
                customer_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                monthly_spend REAL NOT NULL,
                churned INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO customers_raw
                (customer_id, city, monthly_spend, churned)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "Mumbai", 100.0, 0),
                (2, "Mumbai", 200.0, 1),
                (3, "Delhi", 300.0, 0),
            ],
        )


def test_city_kpi_returns_city_metrics(sample_database, capsys):
    result = kpi_city.city_kpi("Mumbai")

    assert result == {
        "customer_count": 2,
        "average_monthly_spend": 150.0,
        "churn_rate": 0.5,
    }
    assert "Mumbai: 2 customers" in capsys.readouterr().out


def test_city_kpi_does_not_run_injection_attempt(sample_database, capsys):
    result = kpi_city.city_kpi("Mumbai' OR 1=1 --")

    assert result is None
    assert "No customers found" in capsys.readouterr().out
