# Generated by Django 5.1.1 on 2024-10-13 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tarificacion', '0004_anexo_estado_codunidad_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='llamada',
            name='tipo_llamada',
            field=models.CharField(choices=[('cel', 'Celular'), ('slm', 'SLM'), ('ldi', 'LDI')], default='cel', max_length=3),
            preserve_default=False,
        ),
    ]