# Generated by Django 3.2.9 on 2021-12-10 13:49

import core.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211210_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='roles',
            new_name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 12, 10, 13, 49, 56, 942427, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to=core.models.img_file_path),
        ),
        migrations.AddField(
            model_name='user',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_by',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
