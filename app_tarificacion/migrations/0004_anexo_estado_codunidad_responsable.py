# Generated by Django 5.1.1 on 2024-10-08 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tarificacion', '0003_remove_codunidad_proveedor_telefonia'),
    ]

    operations = [
        migrations.AddField(
            model_name='anexo',
            name='estado',
            field=models.CharField(choices=[('En servicio', 'En servicio'), ('Fuera de servicio', 'Fuera de servicio')], default='En servicio', max_length=20),
        ),
        migrations.AddField(
            model_name='codunidad',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unidades_responsables', to=settings.AUTH_USER_MODEL),
        ),
    ]