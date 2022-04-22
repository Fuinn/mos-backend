import os
import django.core.management.utils as utils
    
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('MOS_BACKEND_SECRET', utils.get_random_secret_key())

DEBUG = False
if 'MOS_BACKEND_DEBUG' in os.environ:
    debug = os.getenv('MOS_BACKEND_DEBUG')
    if debug == '1':
        DEBUG = True
    elif debug != '0':
        raise ValueError('MOS_BACKEND_DEBUG should be 0 or 1 when provided')

ALLOWED_HOSTS = ['localhost', os.getenv('MOS_BACKEND_HOST', 'localhost')]

CORS_ORIGIN_WHITELIST = [
    'http://{host}:{port}'.format(host=os.getenv('MOS_FRONTEND_HOST', 'localhost'),
                                  port=os.getenv('MOS_FRONTEND_PORT', 4200))           
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'channels',
    'mos.backend',
    'django_cleanup', # should be after all apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'service.urls'

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

WSGI_APPLICATION = 'service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('MOS_DATABASE_NAME', 'postgres'),
        'USER': os.getenv('MOS_DATABASE_USR', 'postgres'),
        'PASSWORD': os.getenv('MOS_DATABASE_PWD', ''),
        'HOST': os.getenv('MOS_DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('MOS_DATABASE_PORT', 5432),
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'UNAUTHENTICATED_USER': None,
}

REDIS_DB = os.getenv('MOS_REDIS_DB', 0)
REDIS_PORT = os.getenv('MOS_REDIS_PORT', 6379)  
REDIS_HOST = os.getenv('MOS_REDIS_HOST', 'localhost')  

RABBIT_PORT = os.getenv('MOS_RABBIT_PORT', 5672)  
RABBIT_USER = os.getenv('MOS_RABBIT_USR', 'guest')
RABBIT_PASS = os.getenv('MOS_RABBIT_PWD', 'guest')
RABBIT_HOST = os.getenv('MOS_RABBIT_HOST', 'localhost')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

EMAIL_HOST = 'mail.fuinn.ie'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('MOS_EMAIL_USR', '')
EMAIL_HOST_PASSWORD = os.getenv('MOS_EMAIL_PWD', '')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'service', 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'service', 'media/')

ASGI_APPLICATION = 'service.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv('MOS_REDIS_HOST', 'localhost'), 
                       os.getenv('MOS_REDIS_PORT', 6379))],
        },
    },
}