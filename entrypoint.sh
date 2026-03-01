#!/bin/bash
set -e

if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
  until python -c "import socket; socket.create_connection(('${DB_HOST}', int('${DB_PORT}')), timeout=2).close()" >/dev/null 2>&1; do
    sleep 1
  done
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 --log-file -
