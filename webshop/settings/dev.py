import socket
from .base import *

try:
	from .local import *
except ImportError:
	pass

DEBUG = True
SECRET_KEY = 'l8a5_lgumyn1=c2%y$1ge1t2u7cce3qup4%dkt7nmm9#ob3l^w'
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['handlers']['celery']['level'] = 'INFO'
LOGGING['handlers']['file']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['celery']['level'] = 'INFO'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'webshop',
		'USER': 'postgres',
		'PASSWORD': 'postgres',
		'HOST': 'postgres',  # 'postgres' '127.0.0.1',
		'PORT': '5432',
	}
}
INSTALLED_APPS += [
	'debug_toolbar',
	# 'livereload',
]
MIDDLEWARE += [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	# 'livereload.middleware.LiveReloadScript',
]

DEBUG_TOOLBAR_CONFIG = {
	# 'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS = [
	'0.0.0.0'
]

REDIS_IP = 'redis'
REDIS_PORT = '6379'
REDIS_ADDRESS = REDIS_IP + ':' + REDIS_PORT
REDIS_PASSWORD = 'redis'
REDIS_DATABASE = '5'


CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://:{password}@{address}/{database}'.format(
	password=REDIS_PASSWORD, address=REDIS_ADDRESS, database=REDIS_DATABASE)

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

BASE_URL = 'http://127.0.0.1:8000'
WAGTAILAPI_BASE_URL = 'http://127.0.0.1:8000/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chobismurf3@gmail.com'
EMAIL_HOST_PASSWORD = 'GRikkaM01314131413!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'chobismurf3@gmail.com'
