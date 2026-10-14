from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Rol, Usuario


@override_settings(AUTH_TOKEN_TTL_MINUTES=25)
class ExpiringTokenTestCase(TestCase):
    def setUp(self):
        role, _ = Rol.objects.get_or_create(nombre_rol='usuario')
        self.user = Usuario.objects.create_user(
            email='expiry-tests@example.test', password='TestOnly-Password123!',
            nombre='Test', apellido='Expiry', id_rol=role,
        )
        self.issued = timezone.now()
        self.token = Token.objects.create(user=self.user)
        Token.objects.filter(pk=self.token.pk).update(created=self.issued)
        self.token.refresh_from_db()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def login(self, client=None):
        return (client or self.client).post('/api/login/', {
            'email': self.user.email, 'contrasena': 'TestOnly-Password123!',
        }, format='json')

    def test_token_is_accepted_before_25_minutes(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=24, seconds=59)):
            response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id_usuario'], self.user.pk)

    def test_token_is_rejected_at_exactly_25_minutes(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=25)):
            response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['WWW-Authenticate'], 'Token')
        self.assertEqual(response.data['detail'].code, 'token_expired')

    def test_token_is_rejected_after_25_minutes(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=26)):
            response = self.client.get('/api/perfil/')
        self.assertEqual(response.status_code, 401)

    def test_activity_does_not_extend_expiry(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=24)):
            self.assertEqual(self.client.get('/api/me/').status_code, 200)
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=25)):
            self.assertEqual(self.client.get('/api/me/').status_code, 401)
        self.token.refresh_from_db()
        self.assertEqual(self.token.created, self.issued)

    def test_login_reuses_a_valid_shared_token_without_extending_expiry(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=20)):
            response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(timezone.datetime.fromisoformat(response.data['expires_at']), self.issued + timedelta(minutes=25))
        self.token.refresh_from_db()
        self.assertEqual(self.token.created, self.issued)

    def test_login_with_expired_header_issues_a_new_token(self):
        now = self.issued + timedelta(minutes=26)
        with patch('api.authentication.timezone.now', return_value=now):
            response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['token'], self.token.key)
        self.assertFalse(Token.objects.filter(pk=self.token.key).exists())
        token = Token.objects.get(user=self.user)
        self.assertEqual(token.created, now)
        self.assertEqual(timezone.datetime.fromisoformat(response.data['expires_at']), now + timedelta(minutes=25))

    def test_login_accepts_invalid_old_header_but_still_requires_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-old-token')
        self.assertEqual(self.login().status_code, 200)
        response = self.client.post('/api/login/', {
            'email': self.user.email, 'contrasena': 'incorrect-test-password',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_registration_ignores_old_header_and_never_grants_admin_role(self):
        admin_role, _ = Rol.objects.get_or_create(nombre_rol='administrador')
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-old-token')
        response = self.client.post('/api/register/', {
            'email': 'registration-expiry@example.test', 'contrasena': 'TestOnly-NewPassword123!',
            'nombre': 'Registration', 'apellido': 'Test', 'id_rol': admin_role.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        user = Usuario.objects.get(email='registration-expiry@example.test')
        self.assertEqual(user.id_rol.nombre_rol, 'usuario')
        self.assertFalse(user.is_superuser)
        self.assertIn('expires_at', response.data)

    def test_unknown_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token unknown-test-token')
        self.assertEqual(self.client.get('/api/me/').status_code, 401)

    def test_inactive_user_token_is_rejected(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        self.assertEqual(self.client.get('/api/me/').status_code, 401)

    def test_missing_token_is_rejected(self):
        self.client.credentials()
        self.assertEqual(self.client.get('/api/me/').status_code, 401)

    def test_logout_revokes_shared_token_for_both_clients(self):
        other = APIClient()
        other.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(other.get('/api/me/').status_code, 200)
        self.assertEqual(self.client.post('/api/logout/').status_code, 200)
        self.assertEqual(other.get('/api/me/').status_code, 401)
        self.assertFalse(Token.objects.filter(pk=self.token.key).exists())

    @override_settings(AUTH_TOKEN_TTL_MINUTES=1)
    def test_configured_lifetime_is_used(self):
        with patch('api.authentication.timezone.now', return_value=self.issued + timedelta(minutes=1)):
            self.assertEqual(self.client.get('/api/me/').status_code, 401)
