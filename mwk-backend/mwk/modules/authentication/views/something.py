import os
import sys
from datetime import timedelta
from pathlib import Path

import environ

# Paths & Initialize environment variables
BASE_DIR = Path(__file__).resolve().parent.parent

# load environment variables from file
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

# Security
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
    # 3rd-party
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

