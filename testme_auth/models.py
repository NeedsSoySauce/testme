from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, EmailValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email: str = None, password: str = None):
        """ Creates and saves a user with the given credentials. """

        # NULL is stored if no email is provided
        if not email:
            email = None
        else:
            email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email
        )

        # A password is generated if none is specified
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """ Creates and saves a superuser with the given credentials. """
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=32, validators=[MinLengthValidator(2)])
    email = models.CharField(unique=True, max_length=254, null=True, validators=[EmailValidator()])

    objects = UserManager()
