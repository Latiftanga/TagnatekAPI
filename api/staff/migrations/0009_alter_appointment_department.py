# Generated by Django 3.2.10 on 2021-12-20 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_rename_job_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='staff.department'),
        ),
    ]
