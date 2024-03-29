"""
Django settings for djangocms project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'baoxsiue+$!avor&00-jhuwx-l*ega+r!!f%36!sluo-hryz^s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# All local hosts
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', '10.5.0.0', '192.168.49.2']

# Application definition

INSTALLED_APPS = [
    'admin_interface', # 3rd party app but it has to load before Django admin
    'colorfield', # 3rd party app but it has to load before Django admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'bootstrap_datepicker_plus',
    'bootstrap4',
    'django_elasticsearch_dsl',
    'corsheaders',

    # Our apps
    'users',
    'homepage',
    'search',
    'upload'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'djangoadmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['djangoadmin/templates/'],
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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth' specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'djangoadmin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "homepage/template/assets"),
)
STATIC_URL = '/static/'

BOOTSTRAP4 = {
    'include_jquery': True,
}

# Login and sign in with Google

path_to_json = "/djangocms/credentials.json"

with open(path_to_json, "r") as handler:
    credentials = json.load(handler)

gmail = credentials["gmail"]
google_api = credentials["google_api"]

# Provider specific settings

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': google_api['client_id'],
            'secret': google_api['secret'],
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 1
LOGIN_REDIRECT_URL = '/users/welcome'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = gmail['username']
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = gmail['username']
EMAIL_HOST_PASSWORD = gmail['password']
EMAIL_PORT = 587

# Save logs into files

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '*': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ************************************************************************
# Kubernetes connections *************************************************
# !IMPORTANT: comment either Kubernetes block or Docker depending of
# which version are you going to use

# PostgreSQL
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.postgresql',
#          'NAME': 'postgres',
#          'USER': 'postgres',
#          'PASSWORD': 'postgres',
#          'HOST': 'postgres-service',
#          'PORT': 5432,
#      }
#  }
#
# # ElasticSearch
#
# ELASTICSEARCH_DSL = {
#      'default': {
#          'hosts': 'elastic-service:9200'
#      },
#  }
#
# # SwiftStack
#
# SWIFT_AUTH_URL = "http://swift-service:8080/auth/v1.0"
# SWIFT_USER = "test"
# SWIFT_PASSWORD = "test"
# SWIFT_CONTAINER = "container"

# ************************************************************************
# Docker connections *****************************************************
# !IMPORTANT: comment either Kubernetes block or Docker depending of
# which version are you going to use

# PostgreSQL
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # SQLite connection
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    # PostgreSQL connection
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# ElasticSearch

ELASTICSEARCH_DSL = {
    'default': {
        # elasticserach:9200 is the docker service and port
       'hosts': os.getenv("ELASTICSEARCH_DSL_HOSTS", 'elasticsearch:9200')
        # 'hosts':'172.19.0.2:9200'
    }
}

# SwiftStack

SWIFT_AUTH_URL = "http://swiftstack:8080/auth/v1.0"
SWIFT_USER = "test"
SWIFT_PASSWORD = "test"
SWIFT_CONTAINER = "container"

# Tika

TIKA_URL = "http://localhost:9998/"