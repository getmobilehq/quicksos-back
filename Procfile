web: gunicorn -b "0.0.0.0:$PORT" -w 3 config.wsgi
release: python manage.py makemigrations
release: python manage.py migrate
