#!/bin/sh
set -e

mkdir -p log data

cd alexandriadocs

python3.4 manage.py collectstatic --noinput
python3.4 manage.py migrate --noinput

exec "$@"
