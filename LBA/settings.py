import os
from pathlib import Path
import dj_database_url
from django.utils.translation import gettext_lazy as _
import socket
import environ

LANGUAGES = [
    ('de', _('German')),
    ('fr', _('French')),
    ('en', _('English')),
]

# Initialize environment variables
env = environ.Env(
    # Set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-nuz3!gby)s_=^-%#(fqi+e4g7jbeltn2o=+bh0o0jm$e!d*m(8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

#ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
#if len(ALLOWED_HOSTS) == 1 and len(ALLOWED_HOSTS[0]) == 0:
#    ALLOWED_HOSTS=['localhost','127.0.0.1','192.168.1.2']
#CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host != 'localhost' and host != '127.0.0.1']

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS=["https://*.aldryn.io"]

## reCAPTCHA configuration
#RECAPTCHA_PUBLIC_KEY = 'your_site_key'  # Replace with your site key
#RECAPTCHA_PRIVATE_KEY = 'your_secret_key'  # Replace with your secret key
#RECAPTCHA_REQUIRED_SCORE = 0.5  # Threshold score (0.0 to 1.0)

DEBUG = env('DEBUG', default='True')
# Development settings for reCAPTCHA (bypassed)
RECAPTCHA_PUBLIC_KEY = 'dummy_public_key'
RECAPTCHA_PRIVATE_KEY = 'dummy_private_key'
RECAPTCHA_REQUIRED_SCORE = 0.5
BYPASS_RECAPTCHA = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'b11_1',
    'storages',
#    'captcha',
    'bootstrap_datepicker_plus',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # This must be after session and before common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'b11_1.utils.middleware.LoginPathMiddleware',
]

ROOT_URLCONF = 'LBA.urls'

HANDLER403 = 'b11_1.views.custom_permission_denied_view'

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
                'django.template.context_processors.i18n',
                'b11_1.utils.context_processors.app_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'LBA.wsgi.application'

#IN_DOCKER = os.environ.get('IN_DOCKER', False)

if "DIVIO_HOSTING" in os.environ:
    DIVIO_HOSTING=True
else:
    DIVIO_HOSTING=False

if "DATABASE_URL" in os.environ and not "DIVIO_HOSTING" in os.environ:
    DOCKER_HOSTING=True
else:
    DOCKER_HOSTING=False

# Database
if DIVIO_HOSTING or DOCKER_HOSTING:
    DATABASES = {'default': dj_database_url.config(conn_max_age=500)}
else:
    # Local development database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'b11-1',
            'USER': 'b11-1_user',
            'PASSWORD': 'b11-1_user',
            'HOST': 'localhost',
            'PORT': '5432',
        },
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'format': '{levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
#            'formatter': 'verbose',
            'formatter': 'simple',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'b11_1.utils.db_log_handler.DatabaseLogHandler',
#            'formatter': 'verbose',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'db'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'b11_1': {
            'handlers': ['console', 'db'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# S3/MinIO settings
if DIVIO_HOSTING:
    # Production settings (Divio S3)
    # source: https://docs.divio.com/reference/work-media-storage/
    AWS_STORAGE_BUCKET_NAME = os.environ.get('DEFAULT_STORAGE_BUCKET', '')
    AWS_ACCESS_KEY_ID = os.environ.get('DEFAULT_STORAGE_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('DEFAULT_STORAGE_SECRET_ACCESS_KEY', '')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('DEFAULT_STORAGE_CUSTOM_DOMAIN', '')
    AWS_S3_REGION_NAME = os.environ.get('DEFAULT_STORAGE_REGION', '')
    AWS_S3_OBJECT_PARAMETERS = {
        'ACL': 'public-read',
        'CacheControl': 'max-age=86400',
    }
    AWS_S3_FILE_OVERWRITE = False
    
    # Default storage settings, with the staticfiles storage updated.
    # See https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-STORAGES
    STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"
    
    if AWS_SECRET_ACCESS_KEY:
      STORAGE_BACKEND = "storages.backends.s3boto3.S3Boto3Storage"
    
    STORAGES = {
        "default": {
            "BACKEND": STORAGE_BACKEND,
        },
        # ManifestStaticFilesStorage is recommended in production, to prevent
        # outdated JavaScript / CSS assets being served from cache
        # See https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        },
    }
    #DEFAULT_STORAGE_BACKEND=s3-storage
    #DEFAULT_STORAGE_BUCKET=beilage111-test-5d283a4e9cd740efae7c4ba-ac86959.divio-media.org
    #DEFAULT_STORAGE_SECRET_ACCESS_KEY=spjuYvdp/Lw85LwQWL1wFk4iKIldYqgmICq91t6s
    #DEFAULT_STORAGE_DSN=s3://AKIA6EOIDQE3KXRV72NA:spjuYvdp%2FLw85LwQWL1wFk4iKIldYqgmICq91t6s@beilage111-test-5d283a4e9cd740efae7c4ba-ac86959.divio-media.org.s3-eu-central-1.amazonaws.com/?auth=s3v4&domain=beilage111-test-5d283a4e9cd740efae7c4ba-ac86959.divio-media.org
    #DEFAULT_STORAGE_REGION=eu-central-1
    #DEFAULT_STORAGE_ACCESS_KEY_ID=AKIA6EOIDQE3KXRV72NA
    #DEFAULT_STORAGE_CUSTOM_DOMAIN=beilage111-test-5d283a4e9cd740efae7c4ba-ac86959.divio-media.org
    #DEFAULT_STORAGE_ENDPOINT_URL=https://s3-eu-central-1.amazonaws.com
    #DEFAULT_STORAGE_ENDPOINT=s3-eu-central-1.amazonaws.com
else:
    # Development settings (MinIO)
    AWS_ACCESS_KEY_ID = 'admin'
    AWS_SECRET_ACCESS_KEY = 'admin123'
    AWS_STORAGE_BUCKET_NAME = 'b11-1'  # Create this bucket in MinIO
    AWS_S3_ENDPOINT_URL = 'http://192.168.1.2:9000'  # MinIO endpoint
    AWS_S3_USE_SSL = False
    AWS_QUERYSTRING_AUTH = False

# Common S3 settings
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Internationalization
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'login_user'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# In settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
#EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
#EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
#EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'yann.crausaz@gmail.com')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
#DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'yann.crausaz@gmail.com')

AUTHENTICATION_BACKENDS = [
    'b11_1.utils.backends.EmailBackend',
    'b11_1.utils.backends.UsernameBackend',
]

# Maximum size for file uploads (in bytes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
