# Generated by Django 5.1.3 on 2024-11-06 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12)),
                ('position', models.CharField(max_length=50)),
                ('establishment', models.CharField(max_length=100)),
                ('holiday_requested_from', models.DateField()),
                ('number_of_days', models.PositiveIntegerField()),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('period', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
