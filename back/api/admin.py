from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Comida,
    Ejercicio,
    PerfilUsuario,
    Plan,
    PlanComida,
    RegistroComidaPlan,
    RegistroEjercicio,
    Rol,
    Rutina,
    Usuario,
    UsuarioPlan,
    UsuarioRutina,
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['id_rol', 'nombre_rol']
    search_fields = ['nombre_rol']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['id_usuario', 'nombre', 'apellido', 'email', 'id_rol', 'is_active', 'is_staff']
    search_fields = ['nombre', 'apellido', 'email']
    list_filter = ['id_rol', 'is_active', 'is_staff', 'fecha_registro']
    ordering = ['email']
    readonly_fields = ['fecha_registro', 'last_login', 'date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Datos personales', {'fields': ('nombre', 'apellido', 'id_rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined', 'fecha_registro')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'nombre',
                'apellido',
                'id_rol',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id_plan', 'nombre_plan', 'objetivo', 'nivel_actividad', 'preferencia_compatible', 'duracion_dias', 'calorias_objetivo', 'activo']
    list_filter = ['objetivo', 'nivel_actividad', 'preferencia_compatible', 'activo']
    search_fields = ['nombre_plan']


@admin.register(Comida)
class ComidaAdmin(admin.ModelAdmin):
    list_display = ['id_comida', 'nombre', 'categoria', 'porcion_referencia', 'calorias', 'proteinas', 'carbohidratos', 'grasas']
    list_filter = ['categoria']
    search_fields = ['nombre']


@admin.register(UsuarioPlan)
class UsuarioPlanAdmin(admin.ModelAdmin):
    list_display = ['id_usuario_plan', 'id_usuario', 'id_plan', 'fecha_inicio', 'fecha_fin', 'estado', 'origen']
    list_filter = ['estado', 'origen']


@admin.register(PlanComida)
class PlanComidaAdmin(admin.ModelAdmin):
    list_display = ['id_plan_comida', 'id_plan', 'dia', 'orden', 'id_comida', 'tipo_comida', 'porcion']
    list_filter = ['id_plan', 'dia', 'tipo_comida']


@admin.register(RegistroComidaPlan)
class RegistroComidaPlanAdmin(admin.ModelAdmin):
    list_display = ['id_registro_comida', 'id_usuario', 'id_plan_comida', 'fecha']
    list_filter = ['fecha']


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_perfil', 'id_usuario', 'objetivo', 'actividad', 'dias_entrenamiento', 'fecha_actualizacion']
    list_filter = ['objetivo', 'actividad', 'preferencia']
    search_fields = ['id_usuario__nombre', 'id_usuario__apellido', 'id_usuario__email']


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['id_rutina', 'nombre', 'objetivo', 'nivel', 'dias_por_semana', 'duracion_semanas', 'activa']
    list_filter = ['objetivo', 'nivel', 'activa']
    search_fields = ['nombre', 'codigo']


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['id_ejercicio', 'id_rutina', 'dia', 'orden', 'nombre']
    list_filter = ['id_rutina', 'dia']
    search_fields = ['nombre']


@admin.register(UsuarioRutina)
class UsuarioRutinaAdmin(admin.ModelAdmin):
    list_display = ['id_usuario_rutina', 'id_usuario', 'id_rutina', 'fecha_asignacion']
    search_fields = ['id_usuario__nombre', 'id_usuario__apellido', 'id_usuario__email']


@admin.register(RegistroEjercicio)
class RegistroEjercicioAdmin(admin.ModelAdmin):
    list_display = ['id_registro_ejercicio', 'id_usuario', 'id_ejercicio', 'fecha']
    list_filter = ['fecha']
    search_fields = ['id_usuario__nombre', 'id_usuario__apellido', 'id_ejercicio__nombre']
