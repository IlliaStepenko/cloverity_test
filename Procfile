release: python manage.py migrate && python manage.py create_demo_user && python manage.py upload_data data/input_data.csv
web: gunicorn cloverity_test.wsgi
