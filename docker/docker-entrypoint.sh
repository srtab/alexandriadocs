#!/bin/sh
set -e

mkdir -p logs data

cd alexandria_docs

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec "$@"
