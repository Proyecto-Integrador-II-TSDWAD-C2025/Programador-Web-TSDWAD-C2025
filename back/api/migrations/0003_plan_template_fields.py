from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_seed_roles_and_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='nivel_actividad',
            field=models.CharField(
                choices=[('baja', 'Baja'), ('moderada', 'Moderada'), ('alta', 'Alta')],
                default='moderada',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='plan',
            name='objetivo',
            field=models.CharField(
                choices=[
                    ('bajar_peso', 'Bajar de peso'),
                    ('mantener_peso', 'Mantener peso'),
                    ('subir_peso', 'Subir de peso'),
                    ('aumentar_masa_muscular', 'Aumentar masa muscular'),
                ],
                default='mantener_peso',
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='plan',
            name='observaciones',
            field=models.TextField(blank=True),
        ),
    ]
