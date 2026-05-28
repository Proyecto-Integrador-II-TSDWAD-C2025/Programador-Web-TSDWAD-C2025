from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Comida, Plan, PlanComida, Rol, Usuario, UsuarioPlan


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
    list_display = ['id_plan', 'nombre_plan', 'duracion_dias', 'calorias_objetivo']
    search_fields = ['nombre_plan']


@admin.register(Comida)
class ComidaAdmin(admin.ModelAdmin):
    list_display = ['id_comida', 'nombre', 'calorias', 'proteinas', 'carbohidratos', 'grasas']
    search_fields = ['nombre']


@admin.register(UsuarioPlan)
class UsuarioPlanAdmin(admin.ModelAdmin):
    list_display = ['id_usuario_plan', 'id_usuario', 'id_plan', 'fecha_inicio', 'fecha_fin', 'estado']
    list_filter = ['estado']


@admin.register(PlanComida)
class PlanComidaAdmin(admin.ModelAdmin):
    list_display = ['id_plan_comida', 'id_plan', 'id_comida', 'tipo_comida']
    list_filter = ['tipo_comida']
