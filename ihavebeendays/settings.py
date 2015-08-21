"""
Django settings for ihavebeendays project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import sys
import dj_database_url
from configurations import Configuration


class Base(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PROJECT_DIR = os.path.join(BASE_DIR, 'ihavebeendays')
    TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates'), )

    sys.path.append(PROJECT_DIR)

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    DEFAULT_SECRET_KEY = ')^h_)$^!@py_ems#1o03kx20*h^$nh%3iw0+s@g0^@kiy39$=e'
    SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = [
        '.herokuapp.com',
    ]

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'social.apps.django_app.default',
        'tastypie',

        'ihavebeendays.core',
        'ihavebeendays.tasks',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.contrib.messages.context_processors.messages',
        'social.apps.django_app.context_processors.backends',
    )

    ROOT_URLCONF = 'ihavebeendays.urls'

    WSGI_APPLICATION = 'ihavebeendays.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, 'static'),
    )

    # Authentication

    AUTHENTICATION_BACKENDS = {
        'social.backends.facebook.FacebookOAuth2',
        'social.backends.google.GoogleOAuth2',

        'django.contrib.auth.backends.ModelBackend',
    }

    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_KEY')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_SECRET')

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.social_auth.associate_by_email',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )

    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
    LOGOUT_URL = '/logout/'


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = True

    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES = Base.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )


class Test(Base):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )


class Prod(Base):
    DATABASES = {
        'default': dj_database_url.config()
    }
