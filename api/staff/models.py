from django.contrib.auth import get_user_model
from django.db import models
from core.models import School


class Gender(models.TextChoices):
    Male = 'M',
    Female = 'F'


class Department(models.Model):
    '''Staff Departments'''
    name = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='jobs'
        )
    description = models.CharField(max_length=128, blank=True)
    institution = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True,
        null=True
        )
    is_current = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.department.name}, {self.start_date} - {self.end_date}'


class Staff(models.Model):
    '''Staff model object'''
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    mobile_phone = models.CharField(max_length=12, blank=True)
    work_phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=64, blank=True)
    jobs = models.ManyToManyField(
        Job,
        related_name='staff',
        blank=True
        )
    staff_id = models.CharField(max_length=16, blank=True)
    registered_no = models.CharField(max_length=16, blank=True)
    sssnit_no = models.CharField(max_length=16, blank=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
        )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='staff',
        null=True,
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.other_names}'

    class Meta:
        ordering = ('first_name', 'last_name', 'other_names')


class Qualification(models.Model):
    '''Teacher academic and prof. qualfications/certificates'''
    ACADEMIC = 'academic'
    PROFESSIONAL = 'professional'
    QUALIFICATION_CHOICES = [
        (ACADEMIC, 'Academic'),
        (PROFESSIONAL, 'Professional'),
        ]
    category = models.CharField(
        max_length=16,
        choices=QUALIFICATION_CHOICES
        )
    title = models.CharField(max_length=64)
    institution = models.CharField(max_length=128)
    date_admitted = models.DateField()
    date_completed = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='qualifications'
        )

    def __str__(self):
        return f'{self.title}, {self.date_admitted} - {self.date_completed}'

    class Meta:
        ordering = ('title', )
