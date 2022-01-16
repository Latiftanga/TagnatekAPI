# Generated by Django 3.2.10 on 2022-01-06 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_student_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='clas',
        ),
        migrations.AddField(
            model_name='student',
            name='klass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='students.class', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardians',
            field=models.ManyToManyField(blank=True, related_name='students', to='students.Guardian'),
        ),
    ]