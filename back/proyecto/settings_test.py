"""Tests locales aislados: SQLite en memoria, sin usar la base MySQL de Railway."""

import os

# Valores exclusivos de tests; no sirven para desplegar ni se conectan a MySQL.
for name, value in {
    'SECRET_KEY': 'test-only-key-not-for-deployment',
    'DB_NAME': 'nutriapp_tests',
    'DB_USER': 'nutriapp_tests',
    'DB_PASSWORD': 'test-only-not-a-real-password',
    'DB_HOST': 'localhost',
    'ALLOWED_HOSTS': 'testserver,localhost,127.0.0.1',
}.items():
    os.environ.setdefault(name, value)

from .settings import *  # noqa: E402,F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
SECURE_HSTS_SECONDS = 0
