# Generated by Django 5.1.1 on 2024-10-18 23:09

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('auth_provider', models.CharField(default='Twilio', max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('last_login_time', models.DateTimeField(auto_now=True)),
                ('is_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('sms_code', models.CharField(blank=True, max_length=6, null=True)),
                ('code_sent_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
