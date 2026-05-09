from django.db import migrations


def seed_roles_and_admin(apps, schema_editor):
    Rol = apps.get_model('api', 'Rol')
    Usuario = apps.get_model('api', 'Usuario')

    rol_admin, _ = Rol.objects.get_or_create(nombre_rol='administrador')
    Rol.objects.get_or_create(nombre_rol='usuario')

    Usuario.objects.get_or_create(
        email='admin@nutriapp.com',
        defaults={
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'contrasena': 'admin123',
            'id_rol': rol_admin,
        },
    )


def reverse_seed(apps, schema_editor):
    Usuario = apps.get_model('api', 'Usuario')
    Rol = apps.get_model('api', 'Rol')

    Usuario.objects.filter(email='admin@nutriapp.com').delete()
    Rol.objects.filter(nombre_rol__in=['administrador', 'usuario']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_roles_and_admin, reverse_seed),
    ]