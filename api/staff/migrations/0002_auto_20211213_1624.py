# Generated by Django 3.2.10 on 2021-12-13 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_school'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={},
        ),
        migrations.AddField(
            model_name='staff',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='core.school'),
            preserve_default=False,
        ),
    ]
