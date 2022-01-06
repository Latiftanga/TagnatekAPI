import os
from django.db import models
from core.models import School
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


def img_file_path(instance, filename):
    """Generate file path for new student logo"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list.
    filename = f'_{instance.id}.{ext}'
    file_path = f'uploads/{instance._meta.model.__name__.lower()}/'
    return os.path.join(file_path, filename)


class Programme(models.Model):
    '''Students programme model'''

    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True
        )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='programmes',
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Class(models.Model):
    '''Programme Divisions'''
    class Grades(models.IntegerChoices):
        FORM_ONE = 1, _('Form 1')
        FORM_TWO = 2, _('Form 2')
        FORM_THREE = 3, _('Form 3')

    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name='classes',
        )
    division = models.CharField(
        max_length=32,
        help_text='Programme division'
        )
    grade = models.PositiveSmallIntegerField(
        choices=Grades.choices
        )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    @property
    def name(self):
        return f'{self.grade}{self.division}'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('grade', )
        unique_together = ('grade', 'division')


class House(models.Model):
    '''Student houses'''

    name = models.CharField(max_length=64, unique=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='houses'
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Guardian(models.Model):
    '''Staff model object'''
    class Gender(models.TextChoices):
        Male = 'M',
        Female = 'F'
    title = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    relation = models.CharField(max_length=64)
    mobile_phone = models.CharField(max_length=12, blank=True)
    home_phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=64, blank=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guardian'
        )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='guardians',
        null=True,
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)


class Student(models.Model):
    '''Staff model object'''
    class Gender(models.TextChoices):
        Male = 'M',
        Female = 'F'

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    mobile_phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=64, blank=True)
    klass = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        related_name='students',
        null=True,
        blank=True,
        verbose_name='class'
        )
    house = models.ForeignKey(
        House,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
        blank=True
        )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
        )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students',
        null=True,
        blank=True
        )
    image = models.ImageField(
        None,
        upload_to=img_file_path,
        blank=True
        )
    guardians = models.ManyToManyField(
        Guardian,
        related_name='students',
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.other_names}'

    class Meta:
        ordering = ('last_name', 'first_name', 'other_names')
