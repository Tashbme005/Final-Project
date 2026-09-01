import os
import urllib.parse
from pathlib import Path

from django.contrib.messages import constants as message_constants
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
ON_VERCEL = os.environ.get('VERCEL') == '1'


def env_flag(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes')


def csv_env(name, default=''):
    return [
        item.strip()
        for item in os.environ.get(name, default).split(',')
        if item.strip()
    ]


def host_from_url(value):
    value = (value or '').strip()
    return value.replace('https://', '').replace('http://', '').split('/')[0]


DEBUG = env_flag('DJANGO_DEBUG', default=not ON_VERCEL)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if DEBUG or ON_VERCEL:
        SECRET_KEY = 'django-insecure-dev-only-change-me'
    else:
        raise ImproperlyConfigured('Set DJANGO_SECRET_KEY when DEBUG is False.')

ALLOWED_HOSTS = csv_env('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
for extra in ('.vercel.app', os.environ.get('VERCEL_URL'), os.environ.get('VERCEL_PROJECT_PRODUCTION_URL')):
    host = host_from_url(extra)
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)
if DEBUG and 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

CSRF_TRUSTED_ORIGINS = csv_env('DJANGO_CSRF_TRUSTED_ORIGINS')
for extra in ('https://*.vercel.app', os.environ.get('VERCEL_URL'), os.environ.get('VERCEL_PROJECT_PRODUCTION_URL')):
    origin = extra if str(extra).startswith('https://') else (f'https://{host_from_url(extra)}' if extra else '')
    if origin and origin not in CSRF_TRUSTED_ORIGINS and origin != 'https://':
        CSRF_TRUSTED_ORIGINS.append(origin)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employees',
    'inventory',
    'orders',
    'payments',
    'services',
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

ROOT_URLCONF = 'oas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'oas' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'employees.context_processors.staff_role',
            ],
        },
    },
]

WSGI_APPLICATION = 'oas.wsgi.application'


def postgres_from_url(database_url):
    url = urllib.parse.urlparse(database_url)
    query = urllib.parse.parse_qs(url.query)
    sslmode = (query.get('sslmode') or ['require'])[0]
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': urllib.parse.unquote(url.path.lstrip('/')),
        'USER': urllib.parse.unquote(url.username or ''),
        'PASSWORD': urllib.parse.unquote(url.password or ''),
        'HOST': url.hostname,
        'PORT': str(url.port or '5432'),
        'CONN_MAX_AGE': 0,
        'OPTIONS': {'sslmode': sslmode},
    }


def database_url_from_env():
    for name in (
        'DATABASE_URL',
        'POSTGRES_URL_NON_POOLING',
        'POSTGRES_URL',
        'POSTGRES_PRISMA_URL',
    ):
        value = (os.environ.get(name) or '').strip()
        if value:
            return value
    return ''


POSTGRES_URL = database_url_from_env()
if POSTGRES_URL:
    DATABASES = {'default': postgres_from_url(POSTGRES_URL)}
elif ON_VERCEL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/oasbay.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

LOGIN_URL = 'home'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
