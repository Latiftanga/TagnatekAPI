# Generated by Django 3.2.10 on 2021-12-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20211217_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
