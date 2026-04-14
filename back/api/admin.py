from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """Admin para gestionar Usuarios"""
    list_display = ['nombre', 'email', 'telefono', 'created_at']
    search_fields = ['nombre', 'email']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
