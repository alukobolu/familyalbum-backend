# Generated by Django 3.1.5 on 2021-12-13 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('type', models.CharField(max_length=5)),
                ('content_text', models.CharField(max_length=1350, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('favourite', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('content_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.files')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('type', models.CharField(max_length=5)),
                ('content_text', models.CharField(max_length=1350, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('favourite', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.albums')),
                ('content_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.files')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedFeeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('permanent_delete', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feeds.comments')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feeds.posts')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feeds.posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='root_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feeds.comments'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
