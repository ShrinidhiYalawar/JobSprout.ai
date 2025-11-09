"""
JobPilot AI - Django Settings Configuration
Complete automation system for job applications
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key-here')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # JobPilot App
    'JobSprout_ai',
    
    # Third party (optional - comment out if not installed)
    # 'rest_framework',
    # 'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',  # Comment out if not using
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# IMPORTANT: Change this to match YOUR project name
# Look at your manage.py file - it shows the correct project name
ROOT_URLCONF = 'job_sprout_project.urls'  # Change this to your actual project name

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

WSGI_APPLICATION = 'job_sprout_project.wsgi.application'  # Change this to your actual project name

# Database
# SQLite for development/small scale (recommended for getting started)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL for production (uncomment when scaling up)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'jobpilot_db'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework (optional - comment out if not installed)
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 50,
# }

# Celery Configuration (NOT NEEDED - We're using GitHub Actions)
# CELERY_BROKER_URL = os.getenv('CELERY_BROKER', 'redis://localhost:6379/0')
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Firebase Configuration
FIREBASE_CONFIG = {
    'credentials_path': BASE_DIR / 'config' / 'firebase_credentials.json',
    'storage_bucket': os.getenv('FIREBASE_BUCKET', 'jobpilot-ai.appspot.com'),
}

# Google Sheets API
GOOGLE_SHEETS_CONFIG = {
    'credentials_path': BASE_DIR / 'config' / 'google_credentials.json',
    'spreadsheet_id': os.getenv('GOOGLE_SHEET_ID', ''),
}

# Gmail API Configuration
GMAIL_CONFIG = {
    'credentials_path': BASE_DIR / 'config' / 'gmail_credentials.json',
    'token_path': BASE_DIR / 'config' / 'gmail_token.json',
}

# Hunter.io API
HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')

# AI API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# JobPilot Automation Settings
JOBPILOT_CONFIG = {
    'max_applications_per_day': 1000,
    'target_ats_score': 80,
    'follow_up_days': 3,
    'auto_apply_enabled': True,
    'recruiter_outreach_enabled': True,
    'search_locations': ['Bengaluru', 'Bangalore', 'Remote', 'Global'],
    'job_portals': [
        'linkedin',
        'naukri',
        'indeed',
        'instahyre',
        'wellfound',
        'company_sites',
    ],
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],  # Only use console for now
        'level': 'INFO',
    },
}

# Create logs directory if it doesn't exist (for future file logging)
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Security (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'