from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-placeholder-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

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

# Database
if config('DATABASE_URL', default=None):
    DATABASES = {
        'default': dj_database_url.config()
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

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
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
    
    # Sidecar for offline Swagger UI
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    
    # API versioning
    'SERVE_URLCONF': None,
    'TAGS': [
        {'name': 'Authentication', 'description': 'User authentication and registration'},
        {'name': 'Tickets', 'description': 'Ticket management operations'},
        {'name': 'Users', 'description': 'User profile management'},
    ],
}