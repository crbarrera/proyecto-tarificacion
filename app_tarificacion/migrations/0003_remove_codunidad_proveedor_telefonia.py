# Generated by Django 5.1.1 on 2024-10-03 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_tarificacion', '0002_rename_ciclotarificacion_ciclo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codunidad',
            name='proveedor_telefonia',
        ),
    ]