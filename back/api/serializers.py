from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers
from .models import (
    Rol,
    Usuario,
    PerfilUsuario,
    Plan,
    Comida,
    UsuarioPlan,
    PlanComida,
    RegistroComidaPlan,
    Rutina,
    Ejercicio,
    UsuarioRutina,
    RegistroEjercicio,
    HistorialPeso,
)
from .permissions import user_has_role
from .nutrition_recommendations import calcular_requerimientos_nutricionales


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

    def validate(self, attrs):
        duracion_dias = attrs.get('duracion_dias', getattr(self.instance, 'duracion_dias', None))
        calorias_objetivo = attrs.get('calorias_objetivo', getattr(self.instance, 'calorias_objetivo', None))

        if duracion_dias is not None and not 1 <= duracion_dias <= 365:
            raise serializers.ValidationError({'duracion_dias': 'La duracion debe estar entre 1 y 365 dias.'})

        if calorias_objetivo is not None and not 500 <= calorias_objetivo <= 6000:
            raise serializers.ValidationError({'calorias_objetivo': 'Las calorias deben estar entre 500 y 6000 kcal.'})

        return attrs


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

    def validate(self, attrs):
        dia = attrs.get('dia', getattr(self.instance, 'dia', None))
        orden = attrs.get('orden', getattr(self.instance, 'orden', None))

        if dia is not None and not 1 <= dia <= 7:
            raise serializers.ValidationError({'dia': 'El dia debe estar entre 1 y 7.'})

        if orden is not None and not 1 <= orden <= 10:
            raise serializers.ValidationError({'orden': 'El orden debe estar entre 1 y 10.'})

        return attrs


class PlanComidaReadSerializer(serializers.ModelSerializer):
    id_comida = ComidaSerializer(read_only=True)
    completada_hoy = serializers.SerializerMethodField()

    class Meta:
        model = PlanComida
        fields = [
            'id_plan_comida',
            'id_plan',
            'id_comida',
            'dia',
            'orden',
            'tipo_comida',
            'porcion',
            'alternativa',
            'completada_hoy',
        ]

    def get_completada_hoy(self, comida_plan):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False

        return RegistroComidaPlan.objects.filter(
            id_usuario=request.user,
            id_plan_comida=comida_plan,
            fecha=timezone.localdate(),
        ).exists()


class PlanDetalleReadSerializer(serializers.ModelSerializer):
    comidas_plan = PlanComidaReadSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = '__all__'


class UsuarioPlanDetalleReadSerializer(serializers.ModelSerializer):
    plan = PlanDetalleReadSerializer(source='id_plan', read_only=True)

    class Meta:
        model = UsuarioPlan
        fields = [
            'id_usuario_plan',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'origen',
            'motivo',
            'plan',
        ]


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    calorias_objetivo = serializers.SerializerMethodField()
    macronutrientes_objetivo = serializers.SerializerMethodField()

    class Meta:
        model = PerfilUsuario
        exclude = ['id_usuario']
        read_only_fields = ['id_perfil', 'fecha_actualizacion', 'calorias_objetivo', 'macronutrientes_objetivo']

    def get_calorias_objetivo(self, obj):
        return calcular_requerimientos_nutricionales(obj)['calorias_objetivo']

    def get_macronutrientes_objetivo(self, obj):
        reqs = calcular_requerimientos_nutricionales(obj)
        return {
            'proteinas': reqs['proteinas_g'],
            'grasas': reqs['grasas_g'],
            'carbohidratos': reqs['carbohidratos_g'],
        }

    def validate(self, attrs):
        valores = {
            'edad': float(attrs.get('edad', getattr(self.instance, 'edad', 0)) or 0),
            'peso_actual': float(attrs.get('peso_actual', getattr(self.instance, 'peso_actual', 0)) or 0),
            'altura_cm': float(attrs.get('altura_cm', getattr(self.instance, 'altura_cm', 0)) or 0),
            'peso_objetivo': float(attrs.get('peso_objetivo', getattr(self.instance, 'peso_objetivo', 0)) or 0),
            'dias_entrenamiento': int(attrs.get(
                'dias_entrenamiento',
                getattr(self.instance, 'dias_entrenamiento', 0),
            ) or 0),
        }
        
        attrs['sexo'] = attrs.get('sexo', getattr(self.instance, 'sexo', 'm'))

        rangos = {
            'edad': (13, 100, 'La edad debe estar entre 13 y 100 anos.'),
            'peso_actual': (30, 300, 'El peso actual debe estar entre 30 y 300 kg.'),
            'altura_cm': (100, 250, 'La altura debe estar entre 100 y 250 cm.'),
            'peso_objetivo': (30, 300, 'El peso objetivo debe estar entre 30 y 300 kg.'),
            'dias_entrenamiento': (1, 6, 'Los dias disponibles deben estar entre 1 y 6.'),
        }

        errores = {}
        for campo, (minimo, maximo, mensaje) in rangos.items():
            valor = valores[campo]
            if valor is not None and not minimo <= valor <= maximo:
                errores[campo] = mensaje

        if errores:
            raise serializers.ValidationError(errores)

        return attrs


class HistorialPesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPeso
        fields = ['id_historial', 'id_usuario', 'peso', 'fecha']
        read_only_fields = ['id_historial', 'id_usuario']



class EjercicioReadSerializer(serializers.ModelSerializer):
    completado_hoy = serializers.SerializerMethodField()

    class Meta:
        model = Ejercicio
        fields = [
            'id_ejercicio',
            'dia',
            'orden',
            'nombre',
            'descripcion',
            'series',
            'repeticiones',
            'duracion_minutos',
            'completado_hoy',
        ]

    def get_completado_hoy(self, ejercicio):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False

        return RegistroEjercicio.objects.filter(
            id_usuario=request.user,
            id_ejercicio=ejercicio,
            fecha=timezone.localdate(),
        ).exists()


class RutinaReadSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioReadSerializer(many=True, read_only=True)

    class Meta:
        model = Rutina
        fields = [
            'id_rutina',
            'nombre',
            'descripcion',
            'objetivo',
            'nivel',
            'dias_por_semana',
            'duracion_semanas',
            'ejercicios',
        ]


class UsuarioRutinaReadSerializer(serializers.ModelSerializer):
    rutina = RutinaReadSerializer(source='id_rutina', read_only=True)

    class Meta:
        model = UsuarioRutina
        fields = ['id_usuario_rutina', 'motivo', 'fecha_asignacion', 'rutina']
