from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from parameterized import parameterized

from quizzes.tests import create_api_response, create_question, MockedTestCase, create_answer, UserAuthTestsMixin


class AnswerTests(MockedTestCase, UserAuthTestsMixin):
    def setUp(self) -> None:
        self.setUpTestUsers()
        self.question = create_question()

    def test_list_view_empty(self):
        """ Returns an empty array when there are no results. """
        expected = create_api_response(
            data={
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            })

        response = self.client.get('/api/answers', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_list_view_non_empty(self):
        """ Returns all answers when no id is given. """
        create_answer(self.question, True)
        create_answer(self.question, False)

        expected = create_api_response(
            data={'count': 2,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'is_correct_answer': True,
                       'question': 'http://testserver/api/questions/1/',
                       'text': 'answer',
                       'url': 'http://testserver/api/answers/1/',
                       'votes': 0,
                       'creator': None},
                      {'is_correct_answer': False,
                       'question': 'http://testserver/api/questions/1/',
                       'text': 'answer',
                       'url': 'http://testserver/api/answers/2/',
                       'votes': 0,
                       'creator': None}
                  ]})
        self.maxDiff = None

        response = self.client.get('/api/answers', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view(self):
        """ Returns the correct question when a valid id is given. """
        create_answer(self.question, True)
        create_answer(self.question, False)

        expected = create_api_response(
            data={'is_correct_answer': True,
                  'question': 'http://testserver/api/questions/1/',
                  'text': 'answer',
                  'url': 'http://testserver/api/answers/1/',
                  'votes': 0,
                  'creator': None})

        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)

    @parameterized.expand([
        'user',
        'admin',
        'anonymous'
    ])
    def test_create_answer(self, user_field):
        """ Anonymous and authenticated users can create an answer. """
        # Login user
        user = getattr(self, user_field)
        user_url = None

        if not user.is_anonymous:
            user_url = f'http://testserver/api/users/{user.pk}/'
            is_authenticated = self.client.login(username=user.username, password=self.password)
            self.assertTrue(is_authenticated)

        question_url = f'http://testserver/api/questions/{self.question.pk}/'
        expected = create_api_response(201,
                                       "Created",
                                       data={'is_correct_answer': True,
                                             'question': question_url,
                                             'text': 'answer',
                                             'url': 'http://testserver/api/answers/1/',
                                             'votes': 0,
                                             'creator': user_url})

        data = {
            'is_correct_answer': True,
            'question': question_url,
            'text': 'answer'
        }

        response = self.client.post('/api/answers/', data=data)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content.decode(), expected)

    @parameterized.expand([
        'user',
        'admin'
    ])
    def test_update_answer(self, user_field):
        """ Authenticated users can update answers they created. """

        # Login user
        user = getattr(self, user_field)
        user_url = None
        creator = None

        if not user.is_anonymous:
            user_url = f'http://testserver/api/users/{user.pk}/'
            creator = user
            is_authenticated = self.client.login(username=user.username, password=self.password)
            self.assertTrue(is_authenticated)

        create_answer(self.question, True, creator=creator)

        question_url = f'http://testserver/api/questions/{self.question.pk}/'
        expected = create_api_response(200,
                                       "OK",
                                       data={'is_correct_answer': False,
                                             'question': question_url,
                                             'text': 'new text',
                                             'url': 'http://testserver/api/answers/1/',
                                             'votes': 0,
                                             'creator': user_url})

        data = {
            'is_correct_answer': False,
            'question': question_url,
            'text': 'new text'
        }

        response = self.client.put('/api/answers/1/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    @parameterized.expand([
        'user',
        'admin'
    ])
    def test_partial_update_answer(self, user_field):
        """ Authenticated users can partially update answers they created. """

        # Login user
        user = getattr(self, user_field)
        user_url = None
        creator = None

        if not user.is_anonymous:
            user_url = f'http://testserver/api/users/{user.pk}/'
            creator = user
            is_authenticated = self.client.login(username=user.username, password=self.password)
            self.assertTrue(is_authenticated)

        create_answer(self.question, True, creator=creator)

        question_url = f'http://testserver/api/questions/{self.question.pk}/'
        expected = create_api_response(200,
                                       "OK",
                                       data={'is_correct_answer': False,
                                             'question': question_url,
                                             'text': 'new text',
                                             'url': 'http://testserver/api/answers/1/',
                                             'votes': 0,
                                             'creator': user_url})

        data = {
            'is_correct_answer': False,
            'text': 'new text'
        }

        response = self.client.patch('/api/answers/1/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)



    @parameterized.expand([
        'admin',
        'other',
        'anonymous'
    ])
    def test_update_another_users_answer_as_admin(self, other_user_field):
        """ Admin users can update answers created by any user. """

        other = getattr(self, other_user_field)
        user = getattr(self, 'admin')
        user_url = None
        creator = None

        if not other.is_anonymous:
            user_url = f'http://testserver/api/users/{other.pk}/'
            creator = other

        create_answer(self.question, True, creator=creator)

        if not user.is_anonymous:
            is_authenticated = self.client.login(username=user.username, password=self.password)
            self.assertTrue(is_authenticated)

        question_url = f'http://testserver/api/questions/{self.question.pk}/'
        expected = create_api_response(200,
                                       "OK",
                                       data={'is_correct_answer': False,
                                             'question': question_url,
                                             'text': 'new text',
                                             'url': 'http://testserver/api/answers/1/',
                                             'votes': 0,
                                             'creator': user_url})

        data = {
            'is_correct_answer': False,
            'question': question_url,
            'text': 'new text'
        }

        response = self.client.put('/api/answers/1/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    @parameterized.expand([
        'admin',
        'other',
        'anonymous'
    ])
    def test_update_another_users_answer(self, other_user_field):
        """ Authenticated non-admin users cannot update answers created by another user. """

        other = getattr(self, other_user_field)
        user = getattr(self, 'user')
        creator = None

        if not other.is_anonymous:
            creator = other

        create_answer(self.question, True, creator=creator)

        if not user.is_anonymous:
            user_url = f'http://testserver/api/users/{user.pk}/'
            is_authenticated = self.client.login(username=user.username, password=self.password)
            self.assertTrue(is_authenticated)

        question_url = f'http://testserver/api/questions/{self.question.pk}/'
        expected = create_api_response(403,
                                       "Forbidden",
                                       data={'detail': 'You do not have permission to perform this action.'})

        data = {
            'is_correct_answer': False,
            'question': question_url,
            'text': 'new text'
        }

        response = self.client.put('/api/answers/1/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content.decode(), expected)
