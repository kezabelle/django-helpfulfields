# -*- coding: utf-8 -*-
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': None,
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'helpfulfields',
)

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

ROOT_URLCONF = 'test_urls'

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
