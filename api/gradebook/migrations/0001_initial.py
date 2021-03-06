# Generated by Django 3.2.10 on 2022-01-10 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0007_alter_user_school'),
        ('students', '0009_auto_20220106_1611'),
        ('staff', '0010_alter_appointment_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('date', models.DateField(default=True)),
                ('points', models.DecimalField(decimal_places=1, max_digits=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('min_points', models.DecimalField(decimal_places=1, max_digits=4)),
                ('max_points', models.DecimalField(decimal_places=1, max_digits=4)),
                ('remark', models.CharField(max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='years', to='core.school')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='gradebook.year')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='gradebook.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='core.school')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='gradebook.classtype', verbose_name='type')),
                ('periods', models.ManyToManyField(blank=True, related_name='classes', to='gradebook.Period')),
                ('students', models.ManyToManyField(blank=True, related_name='classes', to='students.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='gradebook.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='staff.staff')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='gradebook.term')),
            ],
            options={
                'verbose_name': 'class',
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='AssignmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('points', models.DecimalField(decimal_places=1, max_digits=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_types', to='core.school')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='assignment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='gradebook.assignmenttype'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='students',
            field=models.ManyToManyField(related_name='assignments', through='gradebook.Score', to='students.Student'),
        ),
    ]
