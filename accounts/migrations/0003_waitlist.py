# Generated by Django 3.1.5 on 2021-12-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211101_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='wait_email')),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('joined', models.BooleanField(default=False)),
            ],
        ),
    ]