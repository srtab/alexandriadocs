#!/bin/sh
set -e

mkdir -p logs data

python alexandria_docs/manage.py collectstatic --noinput
python alexandria_docs/manage.py migrate --noinput

exec "$@"
