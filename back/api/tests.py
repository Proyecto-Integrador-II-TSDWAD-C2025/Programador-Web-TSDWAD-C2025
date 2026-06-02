from django.test import TestCase
from rest_framework.test import APIClient

from .models import (
    PerfilUsuario,
    Plan,
    PlanComida,
    RegistroComidaPlan,
    RegistroEjercicio,
    Rol,
    Usuario,
    UsuarioPlan,
    UsuarioRutina,
)


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


class PlanTemplateTestCase(TestCase):
    """Test cases para las plantillas alimenticias reutilizables."""

    def setUp(self):
        rol_usuario = Rol.objects.filter(nombre_rol='usuario').first() or Rol.objects.create(nombre_rol='usuario')
        rol_nutricionista = (
            Rol.objects.filter(nombre_rol='nutricionista').first()
            or Rol.objects.create(nombre_rol='nutricionista')
        )
        self.usuario = Usuario.objects.create_user(
            email='usuario.planes@example.com',
            password='ClaveSegura123!',
            nombre='Usuario',
            apellido='Planes',
            id_rol=rol_usuario,
        )
        self.nutricionista = Usuario.objects.create_user(
            email='nutri.planes@example.com',
            password='ClaveSegura123!',
            nombre='Nutri',
            apellido='Planes',
            id_rol=rol_nutricionista,
        )
        self.plan_activo = Plan.objects.create(
            nombre_plan='Plantilla activa',
            descripcion='Plan visible para usuarios.',
            duracion_dias=30,
            calorias_objetivo=1800,
            objetivo='bajar_grasa',
            nivel_actividad='moderado',
            activo=True,
        )
        self.plan_inactivo = Plan.objects.create(
            nombre_plan='Plantilla borrador',
            descripcion='Plan que todavia requiere revision.',
            duracion_dias=21,
            calorias_objetivo=2200,
            objetivo='aumentar_masa',
            nivel_actividad='alto',
            activo=False,
        )
        self.client = APIClient()

    def test_usuario_only_lists_active_templates(self):
        self.client.force_authenticate(user=self.usuario)

        response = self.client.get('/api/planes/')

        self.assertEqual(response.status_code, 200)
        ids_visibles = [plan['id_plan'] for plan in response.data['results']]
        self.assertIn(self.plan_activo.id_plan, ids_visibles)
        self.assertNotIn(self.plan_inactivo.id_plan, ids_visibles)

    def test_nutricionista_can_list_inactive_templates(self):
        self.client.force_authenticate(user=self.nutricionista)

        response = self.client.get('/api/planes/')

        self.assertEqual(response.status_code, 200)
        ids_visibles = [plan['id_plan'] for plan in response.data['results']]
        self.assertIn(self.plan_activo.id_plan, ids_visibles)
        self.assertIn(self.plan_inactivo.id_plan, ids_visibles)

    def test_nutricionista_can_create_classified_template(self):
        self.client.force_authenticate(user=self.nutricionista)

        response = self.client.post('/api/planes/', {
            'nombre_plan': 'Ganancia muscular inicial',
            'descripcion': 'Base editable para pacientes con entrenamiento de fuerza.',
            'duracion_dias': 28,
            'calorias_objetivo': '2400.00',
            'objetivo': 'aumentar_masa',
            'nivel_actividad': 'alto',
            'observaciones': 'Revisar preferencias antes de asignar.',
            'activo': True,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['objetivo'], 'aumentar_masa')
        self.assertEqual(response.data['nivel_actividad'], 'alto')

    def test_template_rejects_out_of_range_calories(self):
        self.client.force_authenticate(user=self.nutricionista)

        response = self.client.post('/api/planes/', {
            'nombre_plan': 'Plantilla invalida',
            'descripcion': 'No debe persistirse.',
            'duracion_dias': 30,
            'calorias_objetivo': '7000.00',
            'objetivo': 'mantener_peso',
            'nivel_actividad': 'moderado',
            'observaciones': '',
            'activo': True,
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('calorias_objetivo', response.data)


class RutinaRecomendadaTestCase(TestCase):
    """Test cases para el perfil y la recomendacion de rutinas predefinidas."""

    def setUp(self):
        rol_usuario = Rol.objects.filter(nombre_rol='usuario').first() or Rol.objects.create(nombre_rol='usuario')
        self.usuario = Usuario.objects.create_user(
            email='usuario.rutina@example.com',
            password='ClaveSegura123!',
            nombre='Usuario',
            apellido='Rutina',
            id_rol=rol_usuario,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.usuario)
        self.perfil_data = {
            'edad': 30,
            'peso_actual': '78.00',
            'altura_cm': 175,
            'peso_objetivo': '82.00',
            'objetivo': 'aumentar_masa',
            'actividad': 'bajo',
            'preferencia': 'sin_preferencia',
            'dias_entrenamiento': 2,
            'limitaciones': '',
        }

    def test_guardar_perfil_asigna_rutina_segun_objetivo(self):
        response = self.client.put('/api/perfil/', self.perfil_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['requiere_revision'])
        self.assertEqual(response.data['rutina']['rutina']['nombre'], 'Fuerza inicial')
        self.assertTrue(PerfilUsuario.objects.filter(id_usuario=self.usuario).exists())
        self.assertEqual(
            UsuarioRutina.objects.get(id_usuario=self.usuario).id_rutina.codigo,
            'fuerza_inicial',
        )

    def test_limitacion_fisica_deriva_a_revision_profesional(self):
        data = {**self.perfil_data, 'limitaciones': 'Molestia persistente en una rodilla.'}

        response = self.client.put('/api/perfil/', data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['requiere_revision'])
        self.assertIsNone(response.data['rutina'])
        self.assertFalse(UsuarioRutina.objects.filter(id_usuario=self.usuario).exists())

    def test_perfil_menor_de_edad_deriva_a_revision_profesional(self):
        data = {**self.perfil_data, 'edad': 16}

        response = self.client.put('/api/perfil/', data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['requiere_revision'])
        self.assertIsNone(response.data['rutina'])

    def test_usuario_puede_marcar_y_desmarcar_un_ejercicio(self):
        self.client.put('/api/perfil/', self.perfil_data)
        rutina_response = self.client.get('/api/mi-rutina/')
        ejercicio_id = rutina_response.data['asignacion']['rutina']['ejercicios'][0]['id_ejercicio']

        completar_response = self.client.post('/api/mi-rutina/completar-ejercicio/', {
            'ejercicio_id': ejercicio_id,
        })
        self.assertEqual(completar_response.status_code, 200)
        self.assertTrue(completar_response.data['completado_hoy'])
        self.assertTrue(RegistroEjercicio.objects.filter(id_usuario=self.usuario).exists())

        desmarcar_response = self.client.post('/api/mi-rutina/completar-ejercicio/', {
            'ejercicio_id': ejercicio_id,
        })
        self.assertEqual(desmarcar_response.status_code, 200)
        self.assertFalse(desmarcar_response.data['completado_hoy'])
        self.assertFalse(RegistroEjercicio.objects.filter(id_usuario=self.usuario).exists())

    def test_rechaza_dias_disponibles_fuera_de_rango(self):
        data = {**self.perfil_data, 'dias_entrenamiento': 7}

        response = self.client.put('/api/perfil/', data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('dias_entrenamiento', response.data)


class PlanAlimenticioRecomendadoTestCase(TestCase):
    """Test cases para orientaciones alimenticias, menus y seguimiento diario."""

    def setUp(self):
        rol_usuario = Rol.objects.filter(nombre_rol='usuario').first() or Rol.objects.create(nombre_rol='usuario')
        self.usuario = Usuario.objects.create_user(
            email='usuario.alimentacion@example.com',
            password='ClaveSegura123!',
            nombre='Usuario',
            apellido='Alimentacion',
            id_rol=rol_usuario,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.usuario)
        self.perfil_data = {
            'edad': 30,
            'peso_actual': '78.00',
            'altura_cm': 175,
            'peso_objetivo': '73.00',
            'objetivo': 'bajar_grasa',
            'actividad': 'moderado',
            'preferencia': 'sin_preferencia',
            'dias_entrenamiento': 3,
            'limitaciones': '',
            'consideraciones_alimentarias': '',
        }

    def test_guardar_perfil_asigna_plan_orientativo_compatible(self):
        response = self.client.put('/api/perfil/', self.perfil_data)

        self.assertEqual(response.status_code, 200)
        asignacion = UsuarioPlan.objects.get(id_usuario=self.usuario)
        self.assertEqual(asignacion.origen, 'orientativo')
        self.assertEqual(asignacion.id_plan.codigo, 'descenso_equilibrado')

    def test_preferencia_vegetariana_asigna_variante_compatible(self):
        data = {**self.perfil_data, 'preferencia': 'vegetariana'}

        response = self.client.put('/api/perfil/', data)

        self.assertEqual(response.status_code, 200)
        asignacion = UsuarioPlan.objects.get(id_usuario=self.usuario)
        self.assertEqual(asignacion.id_plan.codigo, 'descenso_equilibrado_vegetariano')

    def test_consideracion_alimentaria_deriva_a_revision_profesional(self):
        data = {**self.perfil_data, 'consideraciones_alimentarias': 'Alergia a los frutos secos.'}

        response = self.client.put('/api/perfil/', data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['plan_alimenticio'])
        self.assertIn('alergia', response.data['mensaje_plan_alimenticio'])
        self.assertFalse(UsuarioPlan.objects.filter(id_usuario=self.usuario).exists())

    def test_mi_plan_incluye_menu_organizado(self):
        self.client.put('/api/perfil/', self.perfil_data)

        response = self.client.get('/api/mi-plan-alimenticio/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['requiere_revision'])
        self.assertEqual(response.data['asignacion']['plan']['nombre_plan'], 'Descenso equilibrado')
        self.assertEqual(len(response.data['asignacion']['plan']['comidas_plan']), 12)

    def test_usuario_puede_marcar_y_desmarcar_comida_del_plan(self):
        self.client.put('/api/perfil/', self.perfil_data)
        plan_response = self.client.get('/api/mi-plan-alimenticio/')
        plan_comida_id = plan_response.data['asignacion']['plan']['comidas_plan'][0]['id_plan_comida']

        completar_response = self.client.post('/api/mi-plan-alimenticio/completar-comida/', {
            'plan_comida_id': plan_comida_id,
        })
        self.assertEqual(completar_response.status_code, 200)
        self.assertTrue(completar_response.data['completada_hoy'])
        self.assertTrue(RegistroComidaPlan.objects.filter(id_usuario=self.usuario).exists())

        desmarcar_response = self.client.post('/api/mi-plan-alimenticio/completar-comida/', {
            'plan_comida_id': plan_comida_id,
        })
        self.assertEqual(desmarcar_response.status_code, 200)
        self.assertFalse(desmarcar_response.data['completada_hoy'])
        self.assertFalse(RegistroComidaPlan.objects.filter(id_usuario=self.usuario).exists())

    def test_menu_rechaza_dia_fuera_de_rango(self):
        rol_nutricionista = (
            Rol.objects.filter(nombre_rol='nutricionista').first()
            or Rol.objects.create(nombre_rol='nutricionista')
        )
        nutricionista = Usuario.objects.create_user(
            email='nutri.menu@example.com',
            password='ClaveSegura123!',
            nombre='Nutri',
            apellido='Menu',
            id_rol=rol_nutricionista,
        )
        self.client.force_authenticate(user=nutricionista)
        plan = Plan.objects.get(codigo='habitos_equilibrados')
        comida = plan.comidas_plan.first().id_comida

        response = self.client.post('/api/plan-comidas/', {
            'id_plan': plan.id_plan,
            'id_comida': comida.id_comida,
            'dia': 8,
            'orden': 1,
            'tipo_comida': 'desayuno',
            'porcion': '1 porcion',
            'alternativa': '',
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('dia', response.data)
