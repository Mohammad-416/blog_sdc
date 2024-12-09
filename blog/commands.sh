pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrations blog_app
python manage.py migrate
python manage.py collectstatic