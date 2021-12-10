import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
    )


def profile_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list.
    filename = f'_{instance.id}.{ext}'
    return os.path.join('uploads/users/', filename)


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
        ordering = ('name', )

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Create and save an new user'''
        if not email:
            raise ValueError('Email must be provided to create new user')
        user = self.model(email=self.normalize_email(email), **extra_fields)
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
    image = models.ImageField(None, upload_to=profile_file_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
