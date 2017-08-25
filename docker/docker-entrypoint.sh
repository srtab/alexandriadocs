#!/bin/sh
set -e

mkdir -p log data

cd alexandriadocs

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec "$@"
