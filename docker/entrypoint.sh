#!/bin/sh
set -e

echo "Waiting for database..."
python - <<'PY'
import sys
import time

from sqlalchemy import create_engine, text

from app.core.config import settings

for attempt in range(30):
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database is ready.")
        break
    except Exception as exc:
        print(f"Attempt {attempt + 1}/30: {exc}")
        time.sleep(2)
else:
    sys.exit("Database not available.")
PY

echo "Running migrations..."
alembic upgrade head

echo "Seeding development data..."
python scripts/seed.py

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
