from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
