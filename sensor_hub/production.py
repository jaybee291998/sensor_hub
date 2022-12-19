from sensor_hub.settings import *

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1:5500', 'sensorhub.pythonanywhere.com']

STATIC_ROOT = '/home/sensorhub/sensor_hub/static'

MEDIA_URL = '/media/'

MEDIA_ROOT = '/home/sensorhub/sensor_hub/static/media'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sensorhub$default',
        'USER': 'sensorhub',
        'PASSWORD': "Wubbalubbadubdub291998",
        'HOST': 'sensorhub.mysql.pythonanywhere-services.com',
    }
}