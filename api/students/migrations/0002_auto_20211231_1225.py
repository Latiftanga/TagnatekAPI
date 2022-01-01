# Generated by Django 3.2.10 on 2021-12-31 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_school'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='programmes', to='core.school'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(help_text='Programme division', max_length=32)),
                ('grade', models.PositiveSmallIntegerField(choices=[(1, 'Basic 1'), (2, 'Basic 2'), (3, 'Basic 3'), (4, 'Basic 4'), (5, 'Basic 5'), (6, 'Basic 6'), (7, 'JHS 1'), (8, 'JHS 2'), (9, 'JHS 3'), (10, 'SHS 1'), (11, 'SHS 2'), (12, 'SHS 3')])),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='students.programme')),
            ],
            options={
                'ordering': ('grade',),
                'unique_together': {('grade', 'division')},
            },
        ),
    ]
