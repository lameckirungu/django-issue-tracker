from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-placeholder-change-in-production')


def env_bool(name, default=False):
    value = config(name, default=str(default))
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {'1', 'true', 'yes', 'on'}:
        return True
    if normalized in {'0', 'false', 'no', 'off', ''}:
        return False
    return default


def env_list(name, default=''):
    raw = config(name, default=default)
    return [item.strip() for item in str(raw).split(',') if item.strip()]


DEBUG = env_bool('DEBUG', default=False)

# ALLOWED_HOSTS - include Railway domains and custom domains
allowed_hosts = env_list('ALLOWED_HOSTS', default='localhost,127.0.0.1')
# Add Railway domains
allowed_hosts.extend(['.up.railway.app', '.railway.app'])
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts]
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS', default='')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    
    # Local apps
    'apps.accounts',
    'apps.tickets',
    'apps.core',
]

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
database_url = config('DATABASE_URL', default=None)
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default=''),
        }
    }

# Proxy/SSL settings - safe defaults for direct EC2 demo deployment.
USE_X_FORWARDED_HOST = env_bool('USE_X_FORWARDED_HOST', default=False)
if env_bool('USE_PROXY_SSL_HEADER', default=False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', default=False)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', default=False)

# Static files
STATIC_URL = '/static/'
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS = [static_dir]
else:
    STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
}

# OpenAPI/Swagger Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Issue Tracker API',
    'DESCRIPTION': '''
    A full-featured issue tracking system API built with DRF.

    ## Features
    - User authentication with token-based auth
    - Ticket CRUD operations
    - Role-based permissions
    - Status and priority tracking
    - Assignment management

     ## Authentication
    Use Token Authentication by including the header:
    `Authorization: Token <your-token>`
    ''',

    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'CONTACT': {
        'name': 'Lameck',
        'email': 'mugolameck@gmail.com',
        'url': 'https://github.com/lameckirungu/django-issue-tracker',
    },
    'LICENSE': {
        'name': 'MIT License',
        'url': 'https://github.com/lameckirungu/django-issue-tracker/blob/main/LICENSE',
    },
        # Schema customization
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    
    # Swagger UI configuration
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,  # Adds search filter
        'tryItOutEnabled': True,
        'displayRequestDuration': True,
    },
    
    # Security schemes
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Token': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Token-based authentication. Format: `Token <your-token>`'
            },
        }
    },
    'SECURITY': [{'Token': []}],
    
    # CDN docs assets to avoid static manifest/runtime coupling.
    'SWAGGER_UI_DIST': config(
        'SWAGGER_UI_DIST',
        default='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5',
    ),
    'SWAGGER_UI_FAVICON_HREF': config(
        'SWAGGER_UI_FAVICON_HREF',
        default='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/favicon-32x32.png',
    ),
    'REDOC_DIST': config(
        'REDOC_DIST',
        default='https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
    ),
    
    # API versioning
    'SERVE_URLCONF': None,
    'TAGS': [
        {'name': 'Authentication', 'description': 'User authentication and registration'},
        {'name': 'Tickets', 'description': 'Ticket management operations'},
        {'name': 'Users', 'description': 'User profile management'},
    ],
}
