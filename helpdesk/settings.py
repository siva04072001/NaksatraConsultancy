from pathlib import Path
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

env=environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tickets.apps.TicketsConfig',
    'django_celery_results',
    'django_celery_beat',
    'channels',
    'import_export',
]

IMPORT_EXPORT_USE_TRANSACTIONS=True

AUTH_USER_MODEL='tickets.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpdesk.urls'

import os
MEDIA_ROOT = os.path.join(BASE_DIR,'files')
MEDIA_URL = '/files/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'helpdesk.wsgi.application'



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
 }


"""DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE'),
        'NAME':env('POSTGRES_DATABASE'),
        'USER':env('POSTGRES_USER'),
        'PASSWORD':env('POSTGRES_PASSWORD'),
        'HOST':env('POSTGRES_HOST'),
        'PORT':env('POSTGRES_PORT'),
    }
}"""


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


CHANNEL_LAYERS ={
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL','redis://localhost:6379')], 
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/



STATIC_ROOT=os.path.join(BASE_DIR,'assets')

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "svshelpdesk2001@gmail.com"
EMAIL_HOST_PASSWORD = "mwhrruqdvllqxskj"

CELERY_BROKER_URL='redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE='Asia/Kolkata'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'

CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'