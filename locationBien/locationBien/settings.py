"""
Django settings for locationBien project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import  os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #own
    'crispy_forms',
    # 'crispy_bootstrap5',
    'crispy_bootstrap4',
    'users.apps.UsersConfig',
    'gestionBiens',
    'paypal.standard.ipn',
    'widget_tweaks',
    'bootstrap4',
    'anymail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'locationBien.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'locationBien.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': 5432,
    }
    # "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}
# DATABASES = {
#     "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
#     # "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }
# DATABASE_URL = config('DATABASE_URL')


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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



# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Internationalization


AUTH_USER_MODEL = 'users.CustomUser'


# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
# MEDIA_ROOT = os.path.join(BASE_DIR, 'users/medias/users/')



CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
LOGIN_REDIRECT_URL = 'home_without_filter'
# LOGOUT_REDIRECT_URL = 'logout'
#
LOGIN_URL = 'login'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =  config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', 587)
EMAIL_USE_TLS = True


# PAYPAL_CONFIG = {
#     "mode": "sandbox",
#     "client_id": "sb-a5rrc29637788@personal.example.com",
#     "client_secret": "sb-wg7h329637786@business.example.com",
# }
#
# PAYPAL_MODE = "sandbox"
# PAYPAL_REDIRECT_URI = "http://localhost:8000/execute_payment/"
# PAYPAL_CANNEL_URI = "http://localhost:8000/cancel_payment/"
# # Add this line after your other settings :
# NOTIFY_URL = "http://localhost:8000/ipn/"
# # Add this line after your other settings :
# EXPERIENCE_PROFILE_ID = ""
#
# if PAYPAL_MODE == "sandbox":
#     PAYPAL_CLIENT_ID = "sb-a5rrc29637788@personal.example.com"
#     PAYPAL_SECRET = "sb-wg7h329637786@business.example.com"
# else:
#     PAYPAL_CLIENT_ID = "sb-a5rrc29637788@personal.example.com"
#     PAYPAL_SECRET = "sb-wg7h329637786@business.example.com"
#

# PAYPAL_CLIENT_ID = "AcUb_UCmYGIN5ivl6Y9IArqmdprh8bB2dFnPDo1OXI9-LxTgRJpA9gwNxSFg39H9MT4kjO3QooMHqy4l"
# PAYPAL_CLIENT_SECRET = "EMFGnxVn2GbRGADQ-XNaplbt1HITpdb6TERzuJrDFasjH8U0TMd2lgo9jhX929WT2QB2PZz6ua4cLijw"
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')

PAYPAL_MODE = "sandbox"  # "sandbox" or "live"
# URL de retour après le paiement
PAYPAL_RETURN_URL = "execute_payment"

# URL d'annulation du paiement
PAYPAL_CANCEL_URL = "cancel_payment"
# settings.py

###
#stripe paiement
###
STRIPE_PUBLIC_KEY=config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY=config('STRIPE_SECRET_KEY')


# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'amqp://localhost'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# confirmation avant creation de compte
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'



# MEDIA_URL = 'media/'
# # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'staticfiles'),
# ]
# MEDIA_ROOT = os.path.join(BASE_DIR, 'users/medias/users/')
STATIC_URL='static/'
STATIC_ROOT = BASE_DIR/"static"
# STATICFILES_DIRS = [ "static",
# ]
MEDIA_URL = 'media/biens_photos/'
MEDIA_ROOT = BASE_DIR/'media'
