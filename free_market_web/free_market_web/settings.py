"""
Django settings for free_market_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

U_LOG_FILE_SIZE = 1 * 1024 * 1024
U_LOGFILE_COUNT = 5

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'web_logfile': {
            'level': 'DEBUG',
            'maxBytes': U_LOG_FILE_SIZE,
            'backupCount': U_LOGFILE_COUNT,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/../log/web.log',
            'formatter': 'standard',
        },
        'simulator_logfile': {
            'level': 'DEBUG',
            'maxBytes': U_LOG_FILE_SIZE,
            'backupCount': U_LOGFILE_COUNT,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/../log/simulator.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'free_market_web': {
            'handlers': ['web_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'simulation': {
            'handlers': ['simulator_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q403im!5ri2rh^9d(!)jhva@ibf2by068_z7&u1y79_mg^x_$4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'free_market_web',
    'population',
    'accounts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'free_market_web.urls'

WSGI_APPLICATION = 'free_market_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'freemarketdb',
        'USER': 'chaosord',
        'PASSWORD': 'chaosord',
        'HOST': '127.0.0.1'
    }
}

DIRS = [os.path.join(BASE_DIR, app_dir, 'templates') for app_dir in INSTALLED_APPS]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': DIRS,
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                # Insert your
                # # TEMPLATE_CONTEXT_PROCESSORS here or use this
                # # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'free_market_web', 'static'),
)
LOGIN_URL = '/accounts/log_in'
LOGIN_REDIRECT_URL = '/'