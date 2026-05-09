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


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column='id_rol')

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
