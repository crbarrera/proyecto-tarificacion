# Generated by Django 5.1.1 on 2024-10-13 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_tarificacion', '0007_alter_anexo_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='anexo',
            table='app_tarificacion_anexo',
        ),
    ]