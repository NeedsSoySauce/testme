from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, username, email: str = None, password: str = None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        # NULL is stored if no email is provided
        if not email:
            email = None
        else:
            email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **kwargs
        )

        # A password is generated if none is specified
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email: str = None, password: str = None, **kwargs):
        """ Creates and saves a user with the given credentials. """
        return self._create_user(username, email=email, password=password, **kwargs)

    def create_superuser(self, username, email: str = None, password: str = None, **kwargs):
        """ Creates and saves a superuser with the given credentials. """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(username, email=email, password=password, **kwargs)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=32, validators=[MinLengthValidator(2)])
    email = models.EmailField(unique=True, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
