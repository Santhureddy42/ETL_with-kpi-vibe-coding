# Applied Analytics: City Customer KPIs

A small project that loads customer data from a CSV into SQLite and reports city-level customer count, average monthly spend, and churn rate. The city filter uses a parameterized SQL query.

## Project structure

```text
data/
  raw/customers_raw.csv
  db/                  # analytics.db is created by the ETL script
src/
  etl_load_sqlite.py
  kpi_city.py
tests/
  test_kpi_city.py
```

## Run the project

Run these commands from the project root after activating your virtual environment:

```powershell
python -m pip install -r requirements.txt
python src\etl_load_sqlite.py
python src\kpi_city.py
python -m pytest
```

The KPI script reports Mumbai's metrics, then tries a SQL-injection-style city value; the second call finds no matching city.
