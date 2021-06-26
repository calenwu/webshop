"""
Django settings for webshop project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import json
import os
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

with open(PROJECT_DIR + '/settings/secrets.json') as f:
	secrets = json.load(f)

def get_secret(setting, secrets=secrets):
	'''Get the secret variable or return explicit exception.'''
	try:
		return secrets[setting]
	except KeyError:
		error_msg = 'Set the {0} environment variable'.format(setting)
	raise ImproperlyConfigured(error_msg)


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
AUTH_USER_MODEL = 'account.User'
# Application definition

INSTALLED_APPS = [
	'account',

	'wagtail_modeltranslation',
	'wagtail_modeltranslation.makemigrations',
	'wagtail_modeltranslation.migrate',

	'blog',
	'streams',
	'home',
	'shop',
	'coupon',
	'cart',
	'order',
	'contact',
	'newsletter',
	'winwheel',

	'search',
	'wagtail.contrib.search_promotions', #needed for tests to pass
	'wagtail.contrib.forms',
	'wagtail.contrib.modeladmin',  # added
	'wagtail.contrib.redirects',
	'wagtail.contrib.routable_page',  # added
	'wagtail.contrib.settings',  # added
	'wagtail.contrib.sitemaps',  # added
	'wagtail.contrib.styleguide',
	'wagtail.embeds',
	'wagtail.sites',
	'wagtail.users',
	'wagtail.snippets',
	'wagtail.documents',
	'wagtail.images',
	'wagtail.search',
	'wagtail.admin',
	'wagtail.core',
	'wagtail.locales',
	'wagtail.contrib.simple_translation',

	'rosetta',
	'modelcluster',
	'taggit',

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.contrib.sessions.middleware.SessionMiddleware',
	'home.middleware.LanguageMiddleware',
	# 'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'order.middleware.CustomCsrfViewMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'webshop.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
			os.path.join(PROJECT_DIR, 'templates'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.template.context_processors.i18n',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'webshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'webshop',
		'USER': 'postgres',
		'PASSWORD': 'postgres',
		'HOST': 'postgres',
		'PORT': '5432',
	}
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'simple': {
			'format': '%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s'
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'celery': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'celery.log',
			'formatter': 'simple',
			'maxBytes': 1024 * 1024 * 100,  # 100 mb
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'django_error.log',
			'formatter': 'simple',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		}, 
		'celery': {
			'handlers': ['celery', 'console'],
			'level': 'DEBUG',
		},
	},
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
WAGTAIL_I18N_ENABLED = True

USE_TZ = True
LANGUAGES = WAGTAIL_CONTENT_LANGUAGES = [
	('de', _('German')),
	('en', _('English')),
]
LOCALE_PATHS = (PROJECT_DIR + '/locale', )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
	os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Wagtail settings
WAGTAIL_SITE_NAME = 'webshop'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://127.0.0.1:8000'
WAGTAILAPI_BASE_URL = 'http://127.0.0.1:8000/'

# from django.urls import reverse_lazy
# reverse_lazy('account:login')
LOGIN_URL = ''
LOGIN_REDIRECT_URL = ''

WAGTAIL_USER_CREATION_FORM = 'account.forms.CustomUserCreationForm'
WAGTAIL_USER_EDIT_FORM = 'account.forms.CustomUserEditForm'
WAGTAIL_MODERATION_ENABLED = False

CART_SESSION_ID = 'cart'
ORDER_SESSION_ID = 'order'

REDIS_IP = 'redis'
REDIS_PORT = '6379'
REDIS_ADDRESS = REDIS_IP + ':' + REDIS_PORT
REDIS_PASSWORD = 'redis'
REDIS_DATABASE = '5'

CACHES = {
	'default': {
		'BACKEND': "django_redis.cache.RedisCache",
		"LOCATION": 'redis://' + REDIS_ADDRESS + '/' + REDIS_DATABASE,
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
			"PASSWORD": REDIS_PASSWORD
		},
		"KEY_PREFIX": 'webshop'
	}
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chobismurf3@gmail.com'
EMAIL_HOST_PASSWORD = 'GRikkaM01314131413!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'chobismurf3@gmail.com'

# celery settings
CELERY_TIMEZONE = 'Europe/Vienna'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://:{password}@{address}/{database}'.format(
	password=REDIS_PASSWORD, address=REDIS_ADDRESS, database=REDIS_DATABASE)

# wagtail modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'
WAGTAILMODELTRANSLATION_TRANSLATE_SLUGS = False
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'de')
