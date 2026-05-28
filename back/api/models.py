from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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


class Plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    nombre_plan = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    calorias_objetivo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'PLAN'
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return self.nombre_plan


class Comida(models.Model):
    id_comida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
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

    id_usuario_plan = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_column='id_plan')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

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
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_column='id_plan')
    id_comida = models.ForeignKey(Comida, on_delete=models.CASCADE, db_column='id_comida')
    tipo_comida = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        db_table = 'PLAN_COMIDA'
        verbose_name = 'Plan Comida'
        verbose_name_plural = 'Planes Comidas'

    def __str__(self):
        return f"{self.id_plan} - {self.id_comida} ({self.tipo_comida})"
