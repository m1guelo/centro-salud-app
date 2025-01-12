# Generated by Django 5.1.3 on 2024-11-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionrequest',
            name='additional_date_from',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha desde (extra)'),
        ),
        migrations.AddField(
            model_name='permissionrequest',
            name='additional_date_to',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha hasta (extra)'),
        ),
        migrations.AddField(
            model_name='permissionrequest',
            name='anticipado',
            field=models.BooleanField(default=False, verbose_name='Anticipado'),
        ),
        migrations.AddField(
            model_name='permissionrequest',
            name='autorizado',
            field=models.BooleanField(default=False, verbose_name='Autorizado'),
        ),
        migrations.AddField(
            model_name='permissionrequest',
            name='firma_funcionario',
            field=models.FileField(blank=True, null=True, upload_to='firmas/', verbose_name='Firma del funcionario'),
        ),
        migrations.AddField(
            model_name='permissionrequest',
            name='postergado',
            field=models.BooleanField(default=False, verbose_name='Postergado'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='date_from',
            field=models.DateField(verbose_name='Fecha desde'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='date_to',
            field=models.DateField(verbose_name='Fecha hasta'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='establishment',
            field=models.CharField(max_length=100, verbose_name='Establecimiento'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Nombre completo'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='holiday_requested_from',
            field=models.DateField(verbose_name='Solicita feriado desde'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='number_of_days',
            field=models.PositiveIntegerField(verbose_name='Número de días'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='period',
            field=models.CharField(max_length=20, verbose_name='Periodo'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='position',
            field=models.CharField(max_length=50, verbose_name='Cargo'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='rut',
            field=models.CharField(max_length=12, verbose_name='RUT'),
        ),
    ]
