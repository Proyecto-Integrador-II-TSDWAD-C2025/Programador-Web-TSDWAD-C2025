from django.test import TestCase
from rest_framework.test import APIClient

from .models import Rol, Usuario


class UsuarioTestCase(TestCase):
    """Test cases para el modelo Usuario y permisos basicos."""

    def setUp(self):
        self.rol_usuario = Rol.objects.create(nombre_rol='usuario')
        self.rol_admin = Rol.objects.create(nombre_rol='administrador')
        self.rol_nutricionista = Rol.objects.create(nombre_rol='nutricionista')
        self.usuario = Usuario.objects.create_user(
            email='test@example.com',
            password='ClaveSegura123!',
            nombre='Test',
            apellido='Usuario',
            id_rol=self.rol_usuario,
        )
        self.admin = Usuario.objects.create_superuser(
            email='admin@example.com',
            password='Admin123!Seguro',
            nombre='Admin',
            apellido='Sistema',
            id_rol=self.rol_admin,
        )
        self.client = APIClient()

    def test_usuario_creation_hashes_password(self):
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.email, 'test@example.com')
        self.assertTrue(self.usuario.check_password('ClaveSegura123!'))
        self.assertTrue(self.usuario.password.startswith('pbkdf2_'))
        self.assertFalse(hasattr(self.usuario, 'contrasena'))

    def test_test_endpoint(self):
        response = self.client.get('/api/usuarios/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')

    def test_usuario_api_list_requires_authentication(self):
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 401)

    def test_usuario_api_list_allows_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 200)

    def test_crear_nutricionista_requires_admin_role(self):
        self.client.force_authenticate(user=self.usuario)
        response = self.client.post('/api/usuarios/crear-nutricionista/', {
            'nombre': 'Nora',
            'apellido': 'Profesional',
            'email': 'nora@example.com',
            'contrasena': 'ClaveSegura123!',
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_nutricionista_with_hashed_password(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/usuarios/crear-nutricionista/', {
            'nombre': 'Nora',
            'apellido': 'Profesional',
            'email': 'nora@example.com',
            'contrasena': 'ClaveSegura123!',
        })
        self.assertEqual(response.status_code, 201)

        nutricionista = Usuario.objects.get(email='nora@example.com')
        self.assertEqual(nutricionista.id_rol.nombre_rol, 'nutricionista')
        self.assertTrue(nutricionista.check_password('ClaveSegura123!'))
        self.assertTrue(nutricionista.password.startswith('pbkdf2_'))

    def test_nutricionistas_endpoint_only_lists_professionals(self):
        Usuario.objects.create_user(
            email='nutri@example.com',
            password='ClaveSegura123!',
            nombre='Nutri',
            apellido='Prueba',
            id_rol=self.rol_nutricionista,
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.get('/api/usuarios/nutricionistas/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'nutri@example.com')
