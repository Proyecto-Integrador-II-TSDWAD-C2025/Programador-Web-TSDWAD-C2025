from datetime import timedelta

from django.utils import timezone

from .models import Plan, UsuarioPlan


def obtener_revision_alimentaria_requerida(perfil):
    if perfil.edad < 18:
        return True, 'El plan alimenticio debe ser revisado por un profesional porque el perfil corresponde a una persona menor de edad.'

    if perfil.consideraciones_alimentarias.strip():
        return True, 'El plan alimenticio debe ser revisado por un profesional porque indicaste una alergia, intolerancia o consideracion de salud.'

    return False, ''


def obtener_codigo_plan(perfil):
    vegetariano = perfil.preferencia == 'vegetariana'

    if perfil.objetivo == 'bajar_grasa':
        return 'descenso_equilibrado_vegetariano' if vegetariano else 'descenso_equilibrado'

    if perfil.objetivo == 'aumentar_masa':
        return 'apoyo_fuerza_vegetariano' if vegetariano else 'apoyo_fuerza'

    return 'habitos_equilibrados_vegetariano' if vegetariano else 'habitos_equilibrados'


def actualizar_plan_alimenticio_usuario(perfil):
    asignacion_profesional = UsuarioPlan.objects.filter(
        id_usuario=perfil.id_usuario,
        estado='activo',
        origen='profesional',
    ).select_related('id_plan').first()
    if asignacion_profesional:
        return asignacion_profesional, ''

    requiere_revision, mensaje = obtener_revision_alimentaria_requerida(perfil)
    if requiere_revision:
        UsuarioPlan.objects.filter(
            id_usuario=perfil.id_usuario,
            origen='orientativo',
        ).delete()
        return None, mensaje

    plan = Plan.objects.filter(codigo=obtener_codigo_plan(perfil), activo=True).first()
    if plan is None:
        return None, 'Todavia no hay una plantilla alimenticia compatible con tu perfil.'

    fecha_inicio = timezone.localdate()
    fecha_fin = fecha_inicio + timedelta(days=plan.duracion_dias - 1)
    motivo = (
        f'Sugerencia orientativa segun objetivo {perfil.get_objetivo_display().lower()} '
        f'y preferencia {perfil.get_preferencia_display().lower()}.'
    )
    asignacion = UsuarioPlan.objects.filter(
        id_usuario=perfil.id_usuario,
        origen='orientativo',
    ).first()
    if asignacion is None:
        asignacion = UsuarioPlan.objects.create(
            id_usuario=perfil.id_usuario,
            id_plan=plan,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='activo',
            origen='orientativo',
            motivo=motivo,
        )
    elif (
        asignacion.id_plan_id != plan.id_plan
        or asignacion.fecha_inicio != fecha_inicio
        or asignacion.fecha_fin != fecha_fin
        or asignacion.estado != 'activo'
        or asignacion.motivo != motivo
    ):
        asignacion.id_plan = plan
        asignacion.fecha_inicio = fecha_inicio
        asignacion.fecha_fin = fecha_fin
        asignacion.estado = 'activo'
        asignacion.motivo = motivo
        asignacion.save()

    UsuarioPlan.objects.filter(
        id_usuario=perfil.id_usuario,
        origen='orientativo',
    ).exclude(id_usuario_plan=asignacion.id_usuario_plan).delete()
    return asignacion, ''
