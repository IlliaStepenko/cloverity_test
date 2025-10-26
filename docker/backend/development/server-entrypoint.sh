#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py collectstatic --noinput
python manage.py create_demo_user
python manage.py upload_data data/input_data.csv
gunicorn cloverity_test.wsgi:application --bind 0.0.0.0:8000 --reload
