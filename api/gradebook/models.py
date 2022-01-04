from django.db import models
from core.models import School
from staff.models import Staff
from students.models import Student


class Subject(models.Model):
    '''Subject model'''

    name = models.CharField(max_length=32, unique=True)
    short_name = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class Year(models.Model):
    '''School Academic Years'''

    start_date = models.DateField()
    end_date =models.DateField()
    is_active = models.BooleanField(default=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='years'
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    @property
    def name(self):
        return f'{self.start_date.year}/{self.end_date.year}' 

    def __str__(self):
        return self.name


class Class(models.Model):
    '''Class Model'''
    SUBJECT_TYPES = [
        ('core', 'Core'), ('elective', 'Elective')
        ]
    TERM_CHOICES = [
        (1, '1'), (2, '2'), (3, '3')
        ]
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='classes'
        )
    subject_type = models.CharField(max_length=16, choices=SUBJECT_TYPES)
    term = models.PositiveSmallIntegerField(
        choices=TERM_CHOICES
        )
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        related_name='classes'
        )
    teacher = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='classes'
        )
    students = models.ManyToManyField(
        Student,
        related_name='classes',
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    @property
    def name(self):
        return f'{self.subject.name}'

    def __str__(self):
        return self.name
