from django.db import models
from core.models import School
from staff.models import Staff
from students.models import Student


class Subject(models.Model):
    '''Subject model'''

    name = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class Period(models.Model):
    '''Class periods'''

    name = models.CharField(max_length=32, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='periods'
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class Year(models.Model):
    '''School Academic Years'''

    start_date = models.DateField()
    end_date = models.DateField()
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


class Term(models.Model):
    '''School Academic Terms/Sessions'''
    name = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        related_name='terms'
        )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    '''Class Model'''
    CLASS_TYPES = [
        ('core', 'Core'), ('elective', 'Elective')
        ]
    class_type = models.CharField(
        max_length=64,
        choices=CLASS_TYPES,
        verbose_name='type'
        )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='classes'
        )
    term = models.ForeignKey(
        Term,
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
    periods = models.ManyToManyField(
        Period, related_name='classes',
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

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'


class AssignmentType(models.Model):
    '''Assessment Categories Either CA or Exam'''
    NAME_CHOICES = [
        ('CA', 'Continuous Assessment'),
        ('SA', 'Examination')
        ]
    name = models.CharField(
        max_length=2, unique=True,
        choices=NAME_CHOICES
        )
    percentage = models.PositiveSmallIntegerField()
    school = models.ForeignKey(
        School,
        related_name='assignment_types',
        on_delete=models.CASCADE
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.name}'


class Assignment(models.Model):
    '''Assignment model'''

    name = models.CharField(max_length=64, unique=True)
    assessment_type = models.ForeignKey(
        AssignmentType,
        related_name='assignments',
        on_delete=models.CASCADE
        )
    max_points = models.DecimalField(decimal_places=1, max_digits=2)
    students = models.ManyToManyField(
        Student, through='Score',
        related_name='assignments'
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.name}'


class Score(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='scores',
        )
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE,
        related_name='scores'
        )
    mark = models.DecimalField(
        decimal_places=1, max_digits=2,
        null=True,
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.mark}'
