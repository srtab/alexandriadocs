#!/bin/sh
set -e

python alexandria_docs/manage.py collectstatic --noinput
python alexandria_docs/manage.py migrate --noinput

exec "$@"
