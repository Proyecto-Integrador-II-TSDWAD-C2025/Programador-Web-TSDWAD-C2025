import os
import runpy
from pathlib import Path
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.middleware.security import SecurityMiddleware
from django.test import RequestFactory, SimpleTestCase, override_settings


class EnvironmentSettingsTestCase(SimpleTestCase):
    environment = {
        'SECRET_KEY': 'test-only-key-not-for-deployment',
        'ALLOWED_HOSTS': 'api.example.test',
        'DB_NAME': 'nutriapp_tests', 'DB_USER': 'nutriapp_tests',
        'DB_PASSWORD': 'test-only-password', 'DB_HOST': 'localhost',
    }

    def load_settings(self, changes=None, remove=()):
        environment = {**self.environment, **(changes or {})}
        for name in remove:
            environment.pop(name, None)
        with patch.dict(os.environ, environment, clear=True), patch('dotenv.load_dotenv'):
            return runpy.run_path(str(Path(__file__).with_name('settings.py')))

    def test_missing_credentials_fail_without_revealing_values(self):
        for name in ('SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST'):
            with self.subTest(name=name):
                with self.assertRaises(ImproperlyConfigured) as error:
                    self.load_settings(remove=(name,))
                self.assertIn(name, str(error.exception))
                self.assertNotIn(self.environment['DB_PASSWORD'], str(error.exception))

    def test_production_requires_explicit_hosts(self):
        for hosts in ('', '*'):
            with self.subTest(hosts=hosts), self.assertRaises(ImproperlyConfigured):
                self.load_settings({'ALLOWED_HOSTS': hosts})

    def test_production_defaults_to_https_and_secure_cookies(self):
        settings = self.load_settings()
        self.assertFalse(settings['DEBUG'])
        for name in ('SECURE_SSL_REDIRECT', 'SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE'):
            self.assertTrue(settings[name], name)
        self.assertEqual(settings['SECURE_HSTS_SECONDS'], 3600)
        self.assertEqual(settings['CORS_ALLOWED_ORIGINS'], [])
        self.assertNotIn('SECURE_PROXY_SSL_HEADER', settings)

    def test_local_development_uses_http_and_local_origins(self):
        settings = self.load_settings({'DEBUG': ' True '}, remove=('ALLOWED_HOSTS',))
        self.assertFalse(settings['SECURE_SSL_REDIRECT'])
        self.assertFalse(settings['SESSION_COOKIE_SECURE'])
        self.assertFalse(settings['CSRF_COOKIE_SECURE'])
        self.assertEqual(settings['SECURE_HSTS_SECONDS'], 0)
        self.assertIn('http://localhost:4200', settings['CORS_ALLOWED_ORIGINS'])
        self.assertEqual(settings['ALLOWED_HOSTS'], ['localhost', '127.0.0.1'])

    def test_comma_separated_origins_and_proxy_are_configurable(self):
        settings = self.load_settings({
            'CORS_ALLOWED_ORIGINS': ' https://front.example.test, ,https://otro.example.test ',
            'CSRF_TRUSTED_ORIGINS': ' https://front.example.test, ',
            'TRUST_X_FORWARDED_PROTO': 'true',
        })
        self.assertEqual(settings['CORS_ALLOWED_ORIGINS'], ['https://front.example.test', 'https://otro.example.test'])
        self.assertEqual(settings['CSRF_TRUSTED_ORIGINS'], ['https://front.example.test'])
        self.assertEqual(settings['SECURE_PROXY_SSL_HEADER'], ('HTTP_X_FORWARDED_PROTO', 'https'))

    def test_invalid_boolean_is_rejected(self):
        for name in ('DEBUG', 'SECURE_SSL_REDIRECT', 'TRUST_X_FORWARDED_PROTO'):
            with self.subTest(name=name), self.assertRaises(ImproperlyConfigured):
                self.load_settings({name: 'maybe'})

    def test_token_lifetime_defaults_to_25_minutes(self):
        settings = self.load_settings()
        self.assertEqual(settings['AUTH_TOKEN_TTL_MINUTES'], 25)
        self.assertEqual(settings['REST_FRAMEWORK']['DEFAULT_AUTHENTICATION_CLASSES'][0],
                         'api.authentication.ExpiringTokenAuthentication')

    def test_token_lifetime_is_configurable(self):
        self.assertEqual(self.load_settings({'AUTH_TOKEN_TTL_MINUTES': '30'})['AUTH_TOKEN_TTL_MINUTES'], 30)

    def test_invalid_token_lifetime_is_rejected(self):
        for value in ('0', '-1', '25.5', 'invalid'):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                self.load_settings({'AUTH_TOKEN_TTL_MINUTES': value})

    @override_settings(SECURE_SSL_REDIRECT=True, SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'))
    def test_trusted_proxy_does_not_redirect_https_in_a_loop(self):
        request = RequestFactory().get('/api/perfil/', HTTP_X_FORWARDED_PROTO='https')
        middleware = SecurityMiddleware(lambda request: None)
        self.assertIsNone(middleware.process_request(request))

    @override_settings(SECURE_SSL_REDIRECT=True, SECURE_PROXY_SSL_HEADER=None)
    def test_plain_http_redirects_to_https(self):
        request = RequestFactory().get('/api/perfil/', HTTP_HOST='localhost')
        middleware = SecurityMiddleware(lambda request: None)
        response = middleware.process_request(request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, 'https://localhost/api/perfil/')
