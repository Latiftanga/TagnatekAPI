# Generated by Django 3.2.10 on 2022-01-03 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='term',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (1, '2'), (3, '3')]),
        ),
    ]
