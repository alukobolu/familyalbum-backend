# Generated by Django 3.1.5 on 2021-11-01 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='phone',
            new_name='phonenumber',
        ),
    ]