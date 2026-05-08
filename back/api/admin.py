from django.contrib import admin
from .models import Rol, Usuario, Plan, Comida, UsuarioPlan, PlanComida


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['id_rol', 'nombre_rol']
    search_fields = ['nombre_rol']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'nombre', 'apellido', 'email', 'id_rol', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'email']
    list_filter = ['id_rol', 'fecha_registro']
    readonly_fields = ['fecha_registro']


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
