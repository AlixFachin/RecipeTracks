#!/bin/sh

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python3 manage.py makemigrations main --noinput 
python3 manage.py migrate --noinput 
python3 manage.py collectstatic --noinput

exec "$@"
