# Generated by Django 5.1.3 on 2024-11-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0013_alter_compensationrequest_establishment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissionrequest',
            name='holiday_requested_from',
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='additional_date_from',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha desde'),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='additional_date_to',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha hasta'),
        ),
    ]
