#!/bin/sh
set -e

# Wait for Postgres to accept connections before doing anything else.
HOST="${POSTGRES_HOST:-db}"
PORT="${POSTGRES_PORT:-5432}"

echo "Waiting for postgres at ${HOST}:${PORT}..."
while ! nc -z "$HOST" "$PORT"; do
  sleep 0.5
done
echo "Postgres is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"
