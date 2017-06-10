#!/bin/sh
set -e

mkdir -p logs data

cd alexandriadocs

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec "$@"
