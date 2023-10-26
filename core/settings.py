
import environ
from pathlib import Path
import os

env = environ.Env(
    DEBUG = (bool, False),
    ALLOWED_HOSTS = (list, []),
    EMAIL_PORT = (int, 597),
    EMAIL_USE_TLS = (bool, False),
    EMAIL_USE_SSL = (bool, True),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "app",
    "accounts",
    "courses",
    #...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
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

ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /"templates"],
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

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'accounts.CustomUser'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': env.db()
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL= "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


if DEBUG:
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = [STATIC_DIR]

else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


TIME_ZONE = 'Australia/Melbourne'
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")   
EMAIL_PORT = env("EMAIL_PORT") 
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_USE_SSL = env("EMAIL_USE_SSL") 
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD") 
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


 
# All Auth / Social Auth Setting

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_LOGIN_ON_GET = True

# Hubspot
HUBSPOT_API_KEY = env("HUBSPOT_API_KEY")


# stripe settings 
# STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
# STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
# # # Paypal 
# PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID")
# PAYPAL_CLIENT_SECRET = env("PAYPAL_CLIENT_SECRET")
# PAYPAL_MODE = env("PAYPAL_MODE")



# Stripe 
STRIPE_PUBLIC_KEY = 'pk_test_51MaJ5TAcD0sn2XXiwPALdLp15toAqyZmGHtgGt1SxzNredYlrDObKXr8DTuV6aTQjH5IVUDrCuu7IuWuX8QEF8q700ytkMkAuV'
STRIPE_SECRET_KEY = 'sk_test_51MaJ5TAcD0sn2XXirV4BzLJwYPJR1WDXLvEz4T9FI2KhcArCcXKGqvwEtaUfYgSdJBg3c9PKb9vciVMqjnreqzY600UnSM6avQ'


# Paypal 
PAYPAL_CLIENT_ID = 'AUn4dcsOOl1UWbLFfN6igPkWizY-duGcmZDPMXrPY2n-4PNMu4kR8A_hReMVaLkzBlbPPUDPf8IbYpBG'
PAYPAL_CLIENT_SECRET = 'EP0XKKNnsFW9Od8kpR1yh2VJ86qxXBAoIF7B1WgJlR7yqzeif33NR-RxJXm6EiSF7C7Ofr_uAehpzTUI'
PAYPAL_MODE = 'sandbox'  

# Aws S3 
# USE_S3 = env('USE_S3')
# if USE_S3:
#     AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
#     AWS_STORAGE_BUCKET_NAME = 'propstart'
#     AWS_S3_SIGNATURE_NAME = 's3v4'
#     AWS_S3_REGION_NAME = 'eu-north-1'
#     AWS_S3_FILE_OVERWRITE = False
#     AWS_DEFAULT_ACL =  None
#     AWS_S3_VERITY = True
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#     AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {
#         'CacheControl': 'max-age=86400',
#     }
    

