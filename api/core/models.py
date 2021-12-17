import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
    )


def img_file_path(instance, filename):
    """Generate file path for new school logo"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list.
    filename = f'_{instance.id}.{ext}'
    file_path = f'uploads/{instance._meta.model.__name__.lower()}/'
    return os.path.join(file_path, filename)


class School(models.Model):
    '''School Model'''
    name = models.CharField(max_length=128, unique=True)
    motto = models.CharField(max_length=128)
    code = models.CharField(max_length=16, blank=True)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    region = models.CharField(max_length=64)
    phone = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    logo = models.ImageField(
        None,
        upload_to=img_file_path,
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=16, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=16, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name='roles',
        blank=True
        )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


def get_user_role(role_name):
    try:
        role = Role.objects.get(name=role_name)
    except Role.DoesNotExist:
        role = None
    return role


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Create and save an new user'''
        if not email:
            raise ValueError('Email must be provided to create new user')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_teacher(self, email, password=None, **extra_fields):
        '''Create and save an new user'''

        if not email:
            raise ValueError('Email must be provided to create new user')

        role = get_user_role('teacher')

        if not role:
            raise ValueError('Please create teacher Role first')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_admin(self, email, password=None, **extra_fields):
        '''Create and save an new user'''

        if not email:
            raise ValueError('Email must be provided to create new user')

        role = get_user_role('admin')

        if not role:
            raise ValueError('No role name Admin, Create Admin Role first.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = role
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_student(self, email, password=None, **extra_fields):
        '''Create and save an new user'''

        if not email:
            raise ValueError('Email must be provided to create new user')

        role = get_user_role('student')

        if not role:
            raise ValueError('No role name Admin, Create Student Role first.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_parent(self, email, password=None, **extra_fields):
        '''Create and save an new parent'''

        if not email:
            raise ValueError('Email must be provided to create new user')

        role = get_user_role('parent')

        if not role:
            raise ValueError('No role name Parent, Create Student Role first.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user to support email instead username'''

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
        )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
        )
    image = models.ImageField(None, upload_to=img_file_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
