from io import StringIO
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Rol, Usuario


class CrearAdminPruebasTestCase(TestCase):
    email = 'shared-admin-tests@example.test'
    password = 'TestOnly-PrivatePassword123!'

    def run_command(self, passwords=None, **options):
        output = StringIO()
        with patch('api.management.commands.crear_admin_pruebas.sys.stdin.isatty', return_value=True), patch(
            'api.management.commands.crear_admin_pruebas.getpass.getpass',
            side_effect=passwords or [self.password, self.password],
        ):
            call_command('crear_admin_pruebas', email=self.email, stdout=output, **options)
        return output.getvalue()

    def test_creates_role_admin_with_hashed_password_but_no_django_privileges(self):
        output = self.run_command()
        user = Usuario.objects.get(email=self.email)
        self.assertEqual(user.id_rol.nombre_rol, 'administrador')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertNotIn(self.password, output)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_app_admin_can_use_admin_api_with_a_token(self):
        self.run_command()
        client = APIClient()
        response = client.post('/api/login/', {'email': self.email, 'contrasena': self.password}, format='json')
        self.assertEqual(response.status_code, 200)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        self.assertEqual(client.get('/api/usuarios/').status_code, 200)

    def test_does_not_promote_or_overwrite_existing_account(self):
        role, _ = Rol.objects.get_or_create(nombre_rol='usuario')
        user = Usuario.objects.create_user(email=self.email, password=self.password, id_rol=role)
        old_hash = user.password
        with self.assertRaises(CommandError):
            self.run_command()
        user.refresh_from_db()
        self.assertEqual(user.password, old_hash)
        self.assertEqual(user.id_rol, role)

    def test_rejects_mismatched_password_confirmation(self):
        with self.assertRaises(CommandError):
            self.run_command(passwords=[self.password, 'different-test-password'])
        self.assertFalse(Usuario.objects.filter(email=self.email).exists())

    def test_rejects_weak_password(self):
        with self.assertRaises(CommandError):
            self.run_command(passwords=['weak', 'weak'])
        self.assertFalse(Usuario.objects.filter(email=self.email).exists())

    def test_rejects_noninteractive_secret_input(self):
        with patch('api.management.commands.crear_admin_pruebas.sys.stdin.isatty', return_value=False):
            with self.assertRaises(CommandError):
                call_command('crear_admin_pruebas', email=self.email)
        self.assertFalse(Usuario.objects.filter(email=self.email).exists())

    def test_rejects_invalid_email_before_prompting(self):
        with patch('api.management.commands.crear_admin_pruebas.getpass.getpass') as prompt:
            with self.assertRaises(CommandError):
                call_command('crear_admin_pruebas', email='Admin@NutriApp@gmail.com')
        prompt.assert_not_called()
