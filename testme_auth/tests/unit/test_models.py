from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.username = 'asdf12312'
        self.email = 'fizz@buzz.com'
        self.password = 'dsjfio12312'

    def test_create_user(self):
        """ Creating a user with an email works. """
        user = get_user_model().objects.create_user(self.username, self.email, self.password)
        self.assertEqual(user.email, self.email)

    def test_create_user_no_email(self):
        """ Creating a user with no email works and stores NULL as their email in the database. """
        user = get_user_model().objects.create_user(self.username, None, self.password)
        self.assertIsNone(user.email)

    def test_create_user_duplicate_email(self):
        """ Creating a user with an email that's in use fails. """
        _ = get_user_model().objects.create_user(self.username, self.email, self.password)

        with self.assertRaises(IntegrityError):
            _ = get_user_model().objects.create_user(self.username, self.email, self.password)

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(self.username, self.email, self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_no_email(self):
        user = get_user_model().objects.create_superuser(self.username, password=self.password)
        self.assertIsNone(user.email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
