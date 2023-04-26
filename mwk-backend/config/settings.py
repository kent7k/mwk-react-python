import os
import sys
from datetime import timedelta
from pathlib import Path

import environ

# Paths & Initialise environment variables
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    CACHE_BACKEND=(str, 'django.core.cache.backends.filebased.FileBasedCache'),
    CACHE_LOCATION=(str, os.path.join(BASE_DIR, 'cache')),
    SQL_ENGINE=(str, 'django.db.backends.sqlite3'),
    SQL_DATABASE=(str, 'db.sqlite3'),
    SQL_USER=(str, 'user'),
    SQL_PASSWORD=(str, 'password'),
    SQL_HOST=(str, 'localhost'),
    SQL_PORT=(str, '5432'),
)
environ.Env.read_env()

# Services
ROOT_DOMAIN = env('ROOT_DOMAIN', default='localhost')
DEBUG = env.bool('DEBUG', default=True)

# Securities
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    default=[
        'localhost',
        '127.0.0.1',
        '[::1]',
    ],
)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# WSGI
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'config.middlewares.TimezoneMiddleware',
]
WSGI_APPLICATION = 'config.wsgi.application'

# Application definition
PREREQ_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd-parties
    'django_cleanup',
    'debug_toolbar',
    'django_filters',
    'mptt',
    'rest_framework',
    'knox',
    'corsheaders',
    'drf_spectacular',
]

PROJECT_APPS = [
    'mwk.modules.main.apps.MainConfig',
    'mwk.modules.authentication.apps.AuthenticationConfig',
    'mwk.modules.profiles.apps.ProfilesConfig',
]
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'mwk', 'web', 'admin', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# URLs
ROOT_URLCONF = env('ROOT_URLCONF', default='config.urls')

# Database
def get_database_name() -> str:
    if env('SQL_DATABASE') == 'postgresql':
        return env('POSTGRES_DB')
    return 'db.sqlite3'


DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE'),
        'NAME': get_database_name(),
        'USER': env('SQL_USER'),
        'PASSWORD': env('SQL_PASSWORD'),
        'HOST': env('SQL_HOST'),
        'PORT': env('SQL_PORT'),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Caches
CACHES = {
    'default': {
        'BACKEND': env('CACHE_BACKEND'),
        'LOCATION': env('CACHE_LOCATION'),
    },
}

# Email
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Activation email
AUTHENTICATION_SITENAME = 'MWK'
USER_ACTIVATION_URL = env('USER_ACTIVATION_URL') + '{}/{}'

# Internationalization
LANGUAGE_CODE = 'en'
# LANGUAGES = (
#     ('en', _('English')),
#     ('ja', _('Japanese')),
# )
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = env('STATIC_URL', default='static/')

MEDIA_ROOT = env('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))
MEDIA_URL = env('MEDIA_URL', default='/media/')
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 15

TESTS_MEDIA_ROOT = os.path.join(BASE_DIR, 'tests_media')

if 'test' in sys.argv:
    MEDIA_ROOT = TESTS_MEDIA_ROOT
    MEDIA_URL = '/tests-media/'

# Auth `django.contrib.auth`
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]


REST_KNOX = {
    'TOKEN_TTL': timedelta(hours=48),
    'AUTO_REFRESH': True,
    'USER_SERIALIZER': 'mwk.modules.authentication.serializers.LoginPayloadSerializer.LoginPayloadSerializer',
}

# Debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG,
}

# OpenAPI Schema
SPECTACULAR_SETTINGS = {
    'TITLE': 'MWK API',
    'DESCRIPTION': 'MWK API documentation',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# REST framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'mwk.modules.main.pagination.PageParamAPIPagination',
    'PAGE_SIZE': 3,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
