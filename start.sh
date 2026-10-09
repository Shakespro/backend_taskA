#!/bin/sh
set -eu

# Django applies only migrations that are not already recorded in this database.
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Replace this shell with the web server so shutdown signals reach it directly.
exec gunicorn backend.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --access-logfile - \
  --error-logfile -
