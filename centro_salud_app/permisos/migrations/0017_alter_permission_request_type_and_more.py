# Generated by Django 5.1.3 on 2024-11-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0016_permission_created_at_permissionrequest_request_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='request_type',
            field=models.CharField(choices=[('feriado', 'Solicitud de Feriado Legal'), ('administrativo', 'Permiso Administrativo'), ('compensacion', 'Compensación de Tiempo')], default='FERIADO', max_length=20),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='request_type',
            field=models.CharField(choices=[('feriado', 'Solicitud de Feriado Legal'), ('administrativo', 'Permiso Administrativo'), ('compensacion', 'Compensación de Tiempo')], default='FERIADO', max_length=20, verbose_name='Tipo de Solicitud'),
        ),
    ]