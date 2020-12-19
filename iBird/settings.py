"""
Django settings for iBird project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json

# Configuration File
with open('./conf.json', 'r') as f:
    config = json.load(f)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config.get('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'apps.account',
    'apps.prediction',
    'apps.gallery',
    'apps.post'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 临时去除
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iBird.urls'

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

WSGI_APPLICATION = 'iBird.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# MySQL Database Config

MYSQL_DATABASE_NAME = config.get('MYSQL_DATABASE_NAME')
MYSQL_DATABASE_USER = config.get('MYSQL_DATABASE_USER')
MYSQL_DATABASE_PASSWORD = config.get('MYSQL_DATABASE_PASSWORD')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': MYSQL_DATABASE_NAME,
        'USER': MYSQL_DATABASE_USER,
        'PASSWORD': MYSQL_DATABASE_PASSWORD,

        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


# Email Configuration

EMAIL_HOST = config.get('EMAIL_HOST')
EMAIL_PORT = config.get('EMAIL_PORT')
EMAIL_HOST_USER = config.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = config.get('EMAIL_USE_SSL')
EMAIL_USE_TLS = config.get('EMAIL_USE_TLS')
EMAIL_FROM = EMAIL_HOST_USER


# Cache Redis config

REDIS_PASSWORD = config.get('REDIS_PASSWORD')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'decode_responses': True
            },
            'PASSWORD': REDIS_PASSWORD
        }
    }
}


# Constant

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24

# 图片文件允许的拓展名
ALLOWED_IMAGE_EXTENSION = {
    'jpg': "JPEG",
    'jpeg': "JPEG",
    'png': 'PNG'
}

# 图片文件的最大大小 5 MB
IMAGE_MAX_SIZE = 5 * 1024 * 1024

# 存储路径
AVATAR_PATH = 'avatar/'
PICTURE_PATH = 'picture/'

# 鸟类示例图
BIRDS_EXAMPLE_URL = '/birds/{bird_id}.jpg'

IMAGE_USAGE = {
    'a': AVATAR_PATH,
    'p': PICTURE_PATH
}

PHOTOS_PER_PAGE = 12
POST_PER_PAGE = 4

# Verify Code Email Message

VERIFY_CODE_MAIL_MESSAGE = """
以下是你的验证码:
{code}

{username}，你好！
我们收到了来自您的 iBird 账号进行验证的安全请求。请使用上面的验证码进行验证。
请注意：该验证码将于 10 分钟后过期，请尽快验证。

iBird
"""


# Model Config

MODEL_PATH = config.get('MODEL_PATH')
CLASSES_PATH = config.get('CLASSES_PATH')


# RateLimit
# 1 --> 3: Strict Mode --> Loose Mode

RATE_LIMIT_LEVEL_1 = {'block': True, 'key': 'ip', 'rate': '2/2s'}
RATE_LIMIT_LEVEL_2 = {'block': True, 'key': 'ip', 'rate': '2/1s'}
RATE_LIMIT_LEVEL_3 = {'block': True, 'key': 'ip', 'rate': '5/1s'}

# Baidu Map
BAIDU_API_KEY = config.get('BAIDU_API_KEY')
BAIDU_ADDRESS_API_URL = 'http://api.map.baidu.com/geocoder?output=json&location={latitude},{longitude}&ak=' \
                        + BAIDU_API_KEY
