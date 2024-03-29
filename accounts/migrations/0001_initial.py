# Generated by Django 3.1.5 on 2021-11-01 10:58

import accounts.models
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('fullname', models.CharField(max_length=50)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('profile_image', django_resized.forms.ResizedImageField(blank=True, crop=None, default='avatar.png', force_format='JPEG', keep_meta=True, null=True, quality=75, size=[100, 100], upload_to=accounts.models.upload_location)),
                ('registration', models.CharField(default='familyalbum', max_length=100)),
                ('user_city', models.CharField(blank=True, max_length=100, null=True)),
                ('user_country', models.CharField(blank=True, max_length=100, null=True)),
                ('no_files', models.IntegerField(default=0)),
                ('is_blocked', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]
