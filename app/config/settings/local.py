from .base import *

DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.local.application'

INSTALLED_APPS +=[
    'django_extensions',
    'imagekit',
]
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# imagekit 설정
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'config.settings.imagekit-strategy.FixJustInTime'