from django.contrib.auth import get_user_model
from django.test import TestCase
from parameterized import parameterized


class UserViewSetCreateTests(TestCase):
    def setUp(self) -> None:
        self.path = '/api/users/'
        self.username = 'asdf12312'
        self.email = 'fizz@buzz.com'
        self.password = 'dsjfio12312'
        self.data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

        self.expected = {
            'data': {
                'url': 'http://testserver/api/users/1/',
                'username': 'asdf12312',
                'email': 'fizz@buzz.com'
            },
            'message': 'Created',
            'status': 201,
            'success': True
        }

        self.bad_request_response = {
            'message': 'Bad Request',
            'status': 400,
            'success': False
        }

    def test_with_email(self):
        """ Registering a user works with an email specified. """
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/users/1/')
        self.assertJSONEqual(response.content.decode(), self.expected)

    def test_without_email(self):
        """ Registering a user works without an email. """
        response = self.client.post(self.path, {
            'username': self.username,
            'password': self.password
        })

        self.expected['data']['email'] = None

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/users/1/')
        self.assertJSONEqual(response.content.decode(), self.expected)

    def invalid_input_test(self, data, expected):
        """ Helper method for running other tests with invalid input. """
        response = self.client.post(self.path, data)
        self.bad_request_response['data'] = expected
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(), self.bad_request_response)

    @parameterized.expand([
        ({}, {'username': ['This field is required.']}),
        ({'username': ''}, {'username': ['This field may not be blank.']}),
        ({'username': 'a'}, {'username': ['Ensure this field has at least 2 characters.']}),
        ({'username': 'a' * 33}, {'username': ['Ensure this field has no more than 32 characters.']}),
        ({'username': []}, {'username': ['This field is required.']}),
        ({'username': {}}, {'username': ['This field is required.']})
    ])
    def test_invalid_username(self, data, expected):
        """ Correct response returned when an invalid username is supplied. """
        del self.data['username']
        self.data.update(data)
        self.invalid_input_test(self.data, expected)

    @parameterized.expand([
        ({'email': 'fizz'}, {'email': ['Enter a valid email address.']}),
        ({'email': 'fizz@buzz'}, {'email': ['Enter a valid email address.']})
    ])
    def test_invalid_email(self, data, expected):
        """ Correct response returned when an invalid email is supplied. """
        del self.data['email']
        self.data.update(data)
        self.invalid_input_test(self.data, expected)

    @parameterized.expand([
        ({}, {'password': ['This field is required.']}),
        ({'password': ''}, {'password': ['This field may not be blank.']}),
        ({'password': 'onetwo7'}, {'password': ['This password is too short. It must contain at least 8 characters.']}),
        ({'password': ('abc' * 200)[:129]}, {'password': ['Ensure this field has no more than 128 characters.']}),
        ({'password': 'password'}, {'password': ['This password is too common.']}),
        ({'password': '24623187'}, {'password': ['This password is entirely numeric.']}),
        ({'password': []}, {'password': ['This field is required.']}),
        ({'password': {}}, {'password': ['This field is required.']})
    ])
    def test_invalid_password(self, data, expected):
        """ Correct response returned when an invalid password is supplied. """
        del self.data['password']
        self.data.update(data)
        self.invalid_input_test(self.data, expected)

    def test_username_taken(self):
        """ Registration fails if a user with the given username already exists. """
        self.expected = {
            'data': {
                "detail": "This username is unavailable."
            },
            'message': 'OK',
            'status': 200,
            'success': True
        }

        # Create user
        get_user_model().objects.create_user(**self.data)

        # Remove/modify other fields that could conflict
        del self.data['email']

        # Try to create a user with the same username
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), self.expected)

    def test_email_in_use(self):
        """ Registration fails if a user with the given email already exists. """
        self.expected = {
            'data': {
                "detail": "This email is already linked to another account."
            },
            'message': 'OK',
            'status': 200,
            'success': True
        }

        # Create user
        get_user_model().objects.create_user(**self.data)

        # Remove/modify other fields that could conflict
        self.data['username'] += 'abc123'

        # Try to create a user with the same username
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), self.expected)
