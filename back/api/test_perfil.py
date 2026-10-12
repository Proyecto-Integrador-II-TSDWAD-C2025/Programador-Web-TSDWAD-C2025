from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import HistorialPeso, PerfilUsuario, Rol, Usuario, UsuarioPlan, UsuarioRutina


class PerfilPersistenceTestCase(TestCase):
    def setUp(self):
        rol, _ = Rol.objects.get_or_create(nombre_rol='usuario')
        self.usuario = Usuario.objects.create_user(
            email='perfil.prueba@example.com', password='ClaveSegura123!',
            nombre='Perfil', apellido='Prueba', id_rol=rol,
        )
        self.otro_usuario = Usuario.objects.create_user(
            email='perfil.otro@example.com', password='ClaveSegura123!',
            nombre='Otro', apellido='Usuario', id_rol=rol,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.usuario)
        self.data = {
            'sexo': 'm', 'edad': 30, 'peso_actual': '78.00', 'altura_cm': 175,
            'peso_objetivo': '82.00', 'objetivo': 'aumentar_masa', 'actividad': 'bajo',
            'preferencia': 'sin_preferencia', 'dias_entrenamiento': 2,
            'limitaciones': '', 'consideraciones_alimentarias': '',
        }

    def test_perfil_requires_authentication(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get('/api/perfil/').status_code, 401)
        self.assertEqual(self.client.put('/api/perfil/', self.data, format='json').status_code, 401)

    def test_invalid_input_returns_field_errors_and_does_not_write(self):
        with patch('api.views.logger.exception') as log:
            response = self.client.put('/api/perfil/', {**self.data, 'edad': 0}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('edad', response.data)
        self.assertFalse(PerfilUsuario.objects.filter(id_usuario=self.usuario).exists())
        self.assertFalse(HistorialPeso.objects.filter(id_usuario=self.usuario).exists())
        log.assert_not_called()

    def test_save_edit_and_reload_keep_one_daily_weight(self):
        self.assertEqual(self.client.put('/api/perfil/', self.data, format='json').status_code, 200)
        response = self.client.put('/api/perfil/', {**self.data, 'peso_actual': '79.00'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/perfil/').data['perfil']['peso_actual'], '79.00')
        historial = HistorialPeso.objects.get(id_usuario=self.usuario, fecha=timezone.localdate())
        self.assertEqual(historial.peso, Decimal('79.00'))

    def test_malformed_json_still_returns_400_without_writes(self):
        with patch('api.views.logger.exception') as log:
            response = self.client.put('/api/perfil/', '{invalid-json', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(PerfilUsuario.objects.filter(id_usuario=self.usuario).exists())
        log.assert_not_called()

    def test_payload_cannot_modify_another_users_profile(self):
        response = self.client.put('/api/perfil/', {**self.data, 'id_usuario': self.otro_usuario.pk}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PerfilUsuario.objects.filter(id_usuario=self.usuario).exists())
        self.client.force_authenticate(self.otro_usuario)
        self.assertEqual(self.client.get('/api/perfil/').status_code, 404)

    def test_recommendation_failures_return_json_and_rollback_new_profile(self):
        for target in ('actualizar_rutina_usuario', 'actualizar_plan_alimenticio_usuario'):
            with self.subTest(target=target):
                with patch(f'api.views.{target}', side_effect=RuntimeError('internal-only-detail')):
                    with patch('api.views.logger.exception') as log:
                        response = self.client.put('/api/perfil/', self.data, format='json')
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response['Content-Type'], 'application/json')
                self.assertNotIn('internal-only-detail', response.content.decode())
                log.assert_called_once_with('Error al actualizar el perfil del usuario %s', self.usuario.pk)
                for model in (PerfilUsuario, HistorialPeso, UsuarioRutina, UsuarioPlan):
                    self.assertFalse(model.objects.filter(id_usuario=self.usuario).exists(), model.__name__)

    def test_failure_does_not_overwrite_existing_profile_or_daily_weight(self):
        self.assertEqual(self.client.put('/api/perfil/', self.data, format='json').status_code, 200)
        with patch('api.views.actualizar_plan_alimenticio_usuario', side_effect=RuntimeError('failed')):
            with patch('api.views.logger.exception'):
                response = self.client.put('/api/perfil/', {**self.data, 'peso_actual': '79.00'}, format='json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(PerfilUsuario.objects.get(id_usuario=self.usuario).peso_actual, Decimal('78.00'))
        self.assertEqual(HistorialPeso.objects.get(id_usuario=self.usuario).peso, Decimal('78.00'))
