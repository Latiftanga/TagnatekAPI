# Generated by Django 3.2.10 on 2021-12-19 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_auto_20211218_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rank',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='rank',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to='staff.department'),
            preserve_default=False,
        ),
    ]
