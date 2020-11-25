from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from parameterized import parameterized
from rest_framework.test import APIRequestFactory

from testme_auth.permissions import IsSelfOrAdminUserOrReadOnly
from testme_auth.views import UserViewSet


class IsSelfOrAdminUserOrReadOnlyPermissionTests(TestCase):

    def setUp(self) -> None:
        # Setup users
        self.other = get_user_model().objects.create_user("other", password="thisisasecret")
        self.user = get_user_model().objects.create_user("user", password="thisisasecret")
        self.admin = get_user_model().objects.create_superuser("admin", password="thisisasecret")
        self.anonymous = AnonymousUser()

        # Setup request/view for calling permission methods
        self.factory = APIRequestFactory()
        self.path = '/users/'
        self.view = UserViewSet()

        # Dummy data for PUT requests
        self.data = {
            'username': 'test123',
            'email': 'test@test.com',
            'password': 'superdupersecret'
        }

    def put_request_test(self, requester, requested, expected):
        """ Helper for update model tests. """
        request = self.factory.put(self.path + f'/{requested.pk}', data=self.data)
        request.user = requester

        perm = IsSelfOrAdminUserOrReadOnly()
        self.assertEquals(expected, perm.has_object_permission(request, self.view, requested))

    @parameterized.expand([
        'user',
        'admin'
    ])
    def test_update_self(self, user_field):
        """ Authenticated users and admins can update their own user models. """
        user = getattr(self, user_field)
        self.put_request_test(user, user, True)

    @parameterized.expand([
        ('user', False),
        ('admin', True),
        ('anonymous', False)
    ])
    def test_update_other(self, user_field, expected):
        """ Only admins can update user models that are not their own. """
        user = getattr(self, user_field)
        self.put_request_test(user, self.other, expected)

    def get_request_test(self, requester, requested, expected):
        """ Helper for update model tests. """
        request = self.factory.get(self.path + f'/{requested.pk}')
        request.user = requester

        perm = IsSelfOrAdminUserOrReadOnly()
        self.assertEquals(expected, perm.has_object_permission(request, self.view, requested))

    @parameterized.expand([
        'user',
        'admin'
    ])
    def test_can_get_self(self, user_field):
        """ Authenticated users can get/view their own model. """
        user = getattr(self, user_field)
        self.get_request_test(user, user, True)

    @parameterized.expand([
        'user',
        'admin',
        'anonymous'
    ])
    def test_can_get_other(self, user_field):
        """ All users can get/view another user's model. """
        user = getattr(self, user_field)
        self.get_request_test(user, self.other, True)
