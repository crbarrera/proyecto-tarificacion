# Generated by Django 5.1.1 on 2024-10-13 23:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tarificacion', '0009_remove_tarificacion_ciclo_tarificacion_delete_ciclo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarificacion',
            name='codigo_unidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tarificacion.codunidad'),
        ),
    ]