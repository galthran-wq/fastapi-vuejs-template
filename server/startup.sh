#!/bin/bash
set -e

echo "Running database migrations..."
python -m alembic upgrade head
echo "Migrations completed!"
echo "Starting server..."
exec python -m src.main 