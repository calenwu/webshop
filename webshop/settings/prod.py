from .base import *

DEBUG = False

SECRET_KEY = get_secret('SECRET_KEY')

ALLOWED_HOSTS = [
	'127.0.0.1',
	'192.168.1.200',
	'kalunagoods.com'
	'www.kalunagoods.com'
]

# Logging
LOGGING['handlers']['console']['level'] = 'ERROR'
LOGGING['handlers']['celery']['level'] = 'ERROR'
LOGGING['handlers']['file']['level'] = 'ERROR'
LOGGING['loggers']['django']['level'] = 'ERROR'
LOGGING['loggers']['celery']['level'] = 'ERROR'
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'simple': {
			'format': '%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s'
		},
	},
	'handlers': {
		'file': {
			'level': 'WARNING',
			'class': 'logging.FileHandler',
			'filename': os.path.join(BASE_DIR, 'django_error.log'),
			'formatter': 'simple',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['file'],
			'level': 'WARNING',
			'propagate': True,
		},
	},
}

BASE_URL = 'http://127.0.0.1'
WAGTAILAPI_BASE_URL = BASE_URL

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': get_secret('DATABASES_NAME'),
		'USER': get_secret('DATABASES_USER'),
		'PASSWORD': get_secret('DATABASES_PASSWORD'),
		'HOST': get_secret('DATABASES_HOST'),
		'PORT': get_secret('DATABASES_PORT'),
	}
}

REDIS_IP = get_secret('REDIS_IP')
REDIS_PORT = get_secret('REDIS_PORT')
REDIS_ADDRESS = REDIS_IP + ':' + REDIS_PORT
REDIS_PASSWORD = get_secret('REDIS_PASSWORD')
REDIS_DATABASE = get_secret('REDIS_DATABASE')

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://:{password}@{address}/{database}'.format(
	password=REDIS_PASSWORD, address=REDIS_ADDRESS, database=REDIS_DATABASE)

CACHES = {
	'default': {
		'BACKEND': "django_redis.cache.RedisCache",
		"LOCATION": 'redis://' + REDIS_ADDRESS + '/' + REDIS_DATABASE,
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
			"PASSWORD": REDIS_PASSWORD
		},
		"KEY_PREFIX": get_secret('REDIS_KEYPREFIX')
	}
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_secret('EMAIL_PORT')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STATIC_ROOT = '/static/webshop/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/media/webshop/'
MEDIA_URL = '/media/'

