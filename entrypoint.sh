#!/bin/sh

set -e

echo "Waiting for PostgreSQL to become ready..."
export PGPASSWORD=$POSTGRES_PASSWORD
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready!"

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"