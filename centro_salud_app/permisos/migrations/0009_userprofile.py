# Generated by Django 5.1.3 on 2024-11-11 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0008_permissionrequest_estado_permissionrequestadmin_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nombre completo')),
                ('rut', models.CharField(max_length=12, verbose_name='RUT')),
                ('firma', models.ImageField(blank=True, null=True, upload_to='firmas/', verbose_name='Firma')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
