from .models import Rutina, UsuarioRutina


def obtener_revision_requerida(perfil):
    if perfil.edad < 18:
        return True, 'La rutina debe ser revisada por un profesional porque el perfil corresponde a una persona menor de edad.'

    if perfil.limitaciones.strip():
        return True, 'La rutina debe ser revisada por un profesional porque indicaste una limitacion fisica o consideracion de salud.'

    return False, ''


def obtener_codigo_rutina(perfil):
    nivel_inicial = perfil.actividad == 'bajo' or perfil.dias_entrenamiento < 3

    if perfil.objetivo == 'bajar_grasa':
        return 'descenso_gradual' if nivel_inicial else 'descenso_activo'

    if perfil.objetivo == 'aumentar_masa':
        return 'fuerza_inicial' if nivel_inicial else 'fuerza_intermedia'

    if perfil.objetivo == 'mantener_peso':
        return 'inicio_suave' if nivel_inicial else 'bienestar_general'

    return 'inicio_suave' if nivel_inicial else 'bienestar_general'


def actualizar_rutina_usuario(perfil):
    requiere_revision, mensaje = obtener_revision_requerida(perfil)

    if requiere_revision:
        UsuarioRutina.objects.filter(id_usuario=perfil.id_usuario).delete()
        return None, mensaje

    rutina = Rutina.objects.get(codigo=obtener_codigo_rutina(perfil), activa=True)
    motivo = (
        f'Seleccion automatica segun objetivo {perfil.get_objetivo_display().lower()}, '
        f'nivel de actividad {perfil.get_actividad_display().lower()} y '
        f'{perfil.dias_entrenamiento} dias disponibles por semana.'
    )
    asignacion = UsuarioRutina.objects.filter(id_usuario=perfil.id_usuario).first()
    if asignacion is None:
        asignacion = UsuarioRutina.objects.create(
            id_usuario=perfil.id_usuario,
            id_rutina=rutina,
            motivo=motivo,
        )
    elif asignacion.id_rutina_id != rutina.id_rutina or asignacion.motivo != motivo:
        asignacion.id_rutina = rutina
        asignacion.motivo = motivo
        asignacion.save()

    return asignacion, ''
