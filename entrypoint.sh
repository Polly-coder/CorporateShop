#!/usr/bin/env bash
while ! nc -z db 5434; do
    echo "Waiting for database to start..."
    sleep 0.1
done

echo "Database started"

alembic upgrade head
uvicorn app.main:app