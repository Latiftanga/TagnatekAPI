# Generated by Django 3.2.10 on 2021-12-12 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_alter_role_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('other_names', models.CharField(blank=True, max_length=32)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('staff_id', models.CharField(blank=True, max_length=16)),
                ('registered_no', models.CharField(blank=True, max_length=16)),
                ('sssnit_no', models.CharField(blank=True, max_length=16)),
                ('address', models.CharField(blank=True, max_length=128)),
                ('email', models.CharField(blank=True, max_length=64)),
                ('work_phone', models.CharField(blank=True, max_length=12)),
                ('mobile_phone', models.CharField(blank=True, max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='staff.department')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff', to='core.user')),
            ],
            options={
                'ordering': ('first_name', 'last_name', 'other_names'),
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('academic', 'Academic'), ('professional', 'Professional')], max_length=16)),
                ('title', models.CharField(max_length=64)),
                ('institution', models.CharField(max_length=128)),
                ('date_admitted', models.DateField()),
                ('date_completed', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='staff.staff')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
