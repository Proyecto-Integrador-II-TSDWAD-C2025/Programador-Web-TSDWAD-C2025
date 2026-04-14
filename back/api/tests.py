from django.test import TestCase
from rest_framework.test import APIClient
from .models import Usuario


class UsuarioTestCase(TestCase):
    """Test cases para el modelo Usuario"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.usuario = Usuario.objects.create(
            nombre="Test Usuario",
            email="test@example.com",
            telefono="1234567890"
        )
        self.client = APIClient()
    
    def test_usuario_creation(self):
        """Prueba la creación de un usuario"""
        self.assertEqual(self.usuario.nombre, "Test Usuario")
        self.assertEqual(self.usuario.email, "test@example.com")
    
    def test_test_endpoint(self):
        """Prueba el endpoint de conexión a la BD"""
        response = self.client.get('/api/usuarios/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
    
    def test_usuario_api_list(self):
        """Prueba el listado de usuarios"""
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 200)
