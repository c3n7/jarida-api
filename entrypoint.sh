#!/bin/ash

echo "Apply DB Migrations"
python manage.py migrate

exec "$@"