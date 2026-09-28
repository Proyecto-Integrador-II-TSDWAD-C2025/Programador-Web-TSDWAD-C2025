from django.db import migrations


def remove_legacy_seed_admin(apps, schema_editor):
    Usuario = apps.get_model('api', 'Usuario')

    Usuario.objects.filter(
        email='admin@nutriapp.com'
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            'api',
            '0006_perfilusuario_sexo_historialpeso_and_more'
        ),
    ]

    operations = [
        migrations.RunPython(
            remove_legacy_seed_admin,
            migrations.RunPython.noop
        ),
    ]