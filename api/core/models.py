from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
    )


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Create and save an new user'''
        if not email:
            raise ValueError('Email must be provided to create new user')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''Create and save a new superuser'''

        user = self.model(email='super@eg.com', password='super@pass')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user to support email instead username'''

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
