from rest_framework import serializers
from .models import Rol, Usuario, Plan, Comida, UsuarioPlan, PlanComida


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }


class UsuarioReadSerializer(serializers.ModelSerializer):
    id_rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'fecha_registro', 'id_rol']


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class ComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comida
        fields = '__all__'


class UsuarioPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPlan
        fields = '__all__'


class UsuarioPlanReadSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioReadSerializer(read_only=True)
    id_plan = PlanSerializer(read_only=True)

    class Meta:
        model = UsuarioPlan
        fields = '__all__'


class PlanComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanComida
        fields = '__all__'


class PlanComidaReadSerializer(serializers.ModelSerializer):
    id_plan = PlanSerializer(read_only=True)
    id_comida = ComidaSerializer(read_only=True)

    class Meta:
        model = PlanComida
        fields = '__all__'
