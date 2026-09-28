from django.db import migrations


def seed_roles(apps, schema_editor):
    Rol = apps.get_model('api', 'Rol')

    Rol.objects.get_or_create(nombre_rol='administrador')
    Rol.objects.get_or_create(nombre_rol='usuario')
    Rol.objects.get_or_create(nombre_rol='nutricionista')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            seed_roles,
            migrations.RunPython.noop
        ),
    ]