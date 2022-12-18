from sensor_hub.settings import *

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1:5500']

STATIC_ROOT = '/home/jayvee291998/django-finance-app/static'

MEDIA_URL = '/media/'

MEDIA_ROOT = '/home/jayvee291998/django-finance-app/static/media'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jayvee291998$finance',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'jayvee291998.mysql.pythonanywhere-services.com',
    }
}