from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'ROL'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')

        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')
        if not extra_fields.get('id_rol'):
            extra_fields['id_rol'], _ = Rol.objects.get_or_create(nombre_rol='administrador')

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    username = None
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column='id_rol')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    class Meta:
        db_table = 'USUARIO'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class PerfilUsuario(models.Model):
    OBJETIVO_CHOICES = [
        ('bajar_grasa', 'Bajar grasa corporal'),
        ('aumentar_masa', 'Aumentar masa muscular'),
        ('mantener_peso', 'Mantener peso'),
        ('mejorar_habitos', 'Mejorar habitos saludables'),
    ]
    ACTIVIDAD_CHOICES = [
        ('bajo', 'Bajo'),
        ('moderado', 'Moderado'),
        ('alto', 'Alto'),
    ]
    PREFERENCIA_CHOICES = [
        ('sin_preferencia', 'Sin preferencia'),
        ('vegetariana', 'Vegetariana'),
        ('alta_proteina', 'Alta en proteinas'),
        ('baja_calorias', 'Baja en calorias'),
    ]

    id_perfil = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='perfil',
    )
    edad = models.PositiveSmallIntegerField()
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    altura_cm = models.PositiveSmallIntegerField()
    peso_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    objetivo = models.CharField(max_length=30, choices=OBJETIVO_CHOICES)
    actividad = models.CharField(max_length=20, choices=ACTIVIDAD_CHOICES)
    preferencia = models.CharField(max_length=30, choices=PREFERENCIA_CHOICES)
    dias_entrenamiento = models.PositiveSmallIntegerField(default=3)
    limitaciones = models.TextField(blank=True)
    consideraciones_alimentarias = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PERFIL_USUARIO'
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f"Perfil de {self.id_usuario}"


class Plan(models.Model):
    OBJETIVO_CHOICES = [
        ('bajar_grasa', 'Bajar grasa corporal'),
        ('mantener_peso', 'Mantener peso'),
        ('aumentar_masa', 'Aumentar masa muscular'),
        ('mejorar_habitos', 'Mejorar habitos saludables'),
    ]
    NIVEL_ACTIVIDAD_CHOICES = [
        ('bajo', 'Bajo'),
        ('moderado', 'Moderado'),
        ('alto', 'Alto'),
    ]
    PREFERENCIA_CHOICES = [
        ('todas', 'Todas'),
        ('vegetariana', 'Vegetariana'),
        ('alta_proteina', 'Alta en proteinas'),
        ('baja_calorias', 'Baja en calorias'),
    ]

    id_plan = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=60, unique=True, null=True, blank=True)
    nombre_plan = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    calorias_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    objetivo = models.CharField(max_length=30, choices=OBJETIVO_CHOICES, default='mantener_peso')
    nivel_actividad = models.CharField(max_length=20, choices=NIVEL_ACTIVIDAD_CHOICES, default='moderado')
    preferencia_compatible = models.CharField(max_length=30, choices=PREFERENCIA_CHOICES, default='todas')
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'PLAN'
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return self.nombre_plan


class Comida(models.Model):
    CATEGORIA_CHOICES = [
        ('frutas_verduras', 'Frutas y verduras'),
        ('cereales_legumbres', 'Cereales y legumbres'),
        ('proteinas', 'Proteinas'),
        ('lacteos', 'Lacteos'),
        ('grasas_saludables', 'Grasas saludables'),
        ('preparacion', 'Preparacion completa'),
    ]

    id_comida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='preparacion')
    porcion_referencia = models.CharField(max_length=100, default='1 porcion')
    calorias = models.DecimalField(max_digits=10, decimal_places=2)
    proteinas = models.DecimalField(max_digits=10, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=10, decimal_places=2)
    grasas = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'COMIDA'
        verbose_name = 'Comida'
        verbose_name_plural = 'Comidas'

    def __str__(self):
        return self.nombre


class UsuarioPlan(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('completado', 'Completado'),
    ]
    ORIGEN_CHOICES = [
        ('orientativo', 'Orientativo'),
        ('profesional', 'Profesional'),
    ]

    id_usuario_plan = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_column='id_plan')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='profesional')
    motivo = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'USUARIO_PLAN'
        verbose_name = 'Usuario Plan'
        verbose_name_plural = 'Usuarios Planes'

    def __str__(self):
        return f"{self.id_usuario} - {self.id_plan} ({self.estado})"


class PlanComida(models.Model):
    TIPO_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('merienda', 'Merienda'),
        ('cena', 'Cena'),
        ('snack', 'Snack'),
    ]

    id_plan_comida = models.AutoField(primary_key=True)
    id_plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        db_column='id_plan',
        related_name='comidas_plan',
    )
    id_comida = models.ForeignKey(Comida, on_delete=models.CASCADE, db_column='id_comida')
    dia = models.PositiveSmallIntegerField(default=1)
    orden = models.PositiveSmallIntegerField(default=1)
    tipo_comida = models.CharField(max_length=20, choices=TIPO_CHOICES)
    porcion = models.CharField(max_length=100, default='1 porcion')
    alternativa = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'PLAN_COMIDA'
        verbose_name = 'Plan Comida'
        verbose_name_plural = 'Planes Comidas'
        ordering = ['dia', 'orden']

    def __str__(self):
        return f"{self.id_plan} - Dia {self.dia}: {self.id_comida} ({self.tipo_comida})"


class RegistroComidaPlan(models.Model):
    id_registro_comida = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_plan_comida = models.ForeignKey(PlanComida, on_delete=models.CASCADE, db_column='id_plan_comida')
    fecha = models.DateField(default=timezone.localdate)

    class Meta:
        db_table = 'REGISTRO_COMIDA_PLAN'
        verbose_name = 'Registro de comida del plan'
        verbose_name_plural = 'Registros de comidas del plan'
        constraints = [
            models.UniqueConstraint(
                fields=['id_usuario', 'id_plan_comida', 'fecha'],
                name='registro_comida_plan_unico_por_dia',
            ),
        ]

    def __str__(self):
        return f"{self.id_usuario} - {self.id_plan_comida} - {self.fecha}"


class Rutina(models.Model):
    NIVEL_CHOICES = [
        ('inicial', 'Inicial'),
        ('intermedio', 'Intermedio'),
    ]

    id_rutina = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    objetivo = models.CharField(max_length=30, choices=PerfilUsuario.OBJETIVO_CHOICES)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    dias_por_semana = models.PositiveSmallIntegerField()
    duracion_semanas = models.PositiveSmallIntegerField(default=4)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'RUTINA'
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    id_ejercicio = models.AutoField(primary_key=True)
    id_rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        db_column='id_rutina',
        related_name='ejercicios',
    )
    dia = models.PositiveSmallIntegerField()
    orden = models.PositiveSmallIntegerField(default=1)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    series = models.PositiveSmallIntegerField(null=True, blank=True)
    repeticiones = models.CharField(max_length=30, blank=True)
    duracion_minutos = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'EJERCICIO'
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'
        ordering = ['dia', 'orden']

    def __str__(self):
        return f"{self.id_rutina.nombre} - Dia {self.dia}: {self.nombre}"


class UsuarioRutina(models.Model):
    id_usuario_rutina = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='rutina_asignada',
    )
    id_rutina = models.ForeignKey(Rutina, on_delete=models.PROTECT, db_column='id_rutina')
    motivo = models.CharField(max_length=255)
    fecha_asignacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'USUARIO_RUTINA'
        verbose_name = 'Usuario rutina'
        verbose_name_plural = 'Usuarios rutinas'

    def __str__(self):
        return f"{self.id_usuario} - {self.id_rutina}"


class RegistroEjercicio(models.Model):
    id_registro_ejercicio = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, db_column='id_ejercicio')
    fecha = models.DateField(default=timezone.localdate)

    class Meta:
        db_table = 'REGISTRO_EJERCICIO'
        verbose_name = 'Registro de ejercicio'
        verbose_name_plural = 'Registros de ejercicios'
        constraints = [
            models.UniqueConstraint(
                fields=['id_usuario', 'id_ejercicio', 'fecha'],
                name='registro_ejercicio_unico_por_dia',
            ),
        ]

    def __str__(self):
        return f"{self.id_usuario} - {self.id_ejercicio} - {self.fecha}"
