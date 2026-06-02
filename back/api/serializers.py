from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Rol, Usuario, Plan, Comida, UsuarioPlan, PlanComida
from .permissions import user_has_role


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'contrasena', 'id_rol', 'is_active']

    def validate(self, attrs):
        contrasena = attrs.get('contrasena')

        if self.instance is None and not contrasena:
            raise serializers.ValidationError({'contrasena': 'La contrasena es obligatoria.'})

        if contrasena:
            try:
                validate_password(contrasena)
            except DjangoValidationError as exc:
                raise serializers.ValidationError({'contrasena': list(exc.messages)})

        return attrs

    def create(self, validated_data):
        contrasena = validated_data.pop('contrasena')
        usuario = Usuario(**validated_data)
        usuario.set_password(contrasena)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and not user_has_role(request.user, 'administrador'):
            validated_data.pop('id_rol', None)

        contrasena = validated_data.pop('contrasena', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if contrasena:
            instance.set_password(contrasena)

        instance.save()
        return instance


class NutricionistaCreateSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'contrasena']

    def create(self, validated_data):
        rol_nutricionista = Rol.objects.filter(nombre_rol='nutricionista').first()
        if rol_nutricionista is None:
            rol_nutricionista = Rol.objects.create(nombre_rol='nutricionista')

        validated_data['id_rol'] = rol_nutricionista
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    contrasena = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        usuario = authenticate(
            request=self.context.get('request'),
            username=attrs.get('email'),
            password=attrs.get('contrasena'),
        )

        if usuario is None:
            raise serializers.ValidationError({'error': 'Credenciales invalidas.'})

        if not usuario.is_active:
            raise serializers.ValidationError({'error': 'La cuenta esta desactivada.'})

        attrs['usuario'] = usuario
        return attrs


class UsuarioReadSerializer(serializers.ModelSerializer):
    id_rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'fecha_registro', 'id_rol', 'is_active']


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

    def validate(self, attrs):
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise serializers.ValidationError(
                {'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'}
            )
        return attrs


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
