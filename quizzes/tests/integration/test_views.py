from django.test import TestCase

from quizzes.tests import create_tag, create_api_response, create_question, MockedTestCase, create_answer, \
    create_quizzes


class TagsTests(TestCase):
    def test_list_view_empty(self):
        """ Returns an empty array when there are no results. """
        expected = create_api_response(
            data={
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            })

        response = self.client.get('/api/tags', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_list_view_non_empty(self):
        """ Returns all tags when no id is given. """
        create_tag('tag1')
        create_tag('tag2')
        expected = create_api_response(
            data={'count': 2,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'name': 'tag1', 'url': 'http://testserver/api/tags/1/'},
                      {'name': 'tag2', 'url': 'http://testserver/api/tags/2/'}
                  ]})

        response = self.client.get('/api/tags', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view(self):
        """ Returns the correct tag when a valid id is given. """
        create_tag('tag1')
        create_tag('tag2')
        expected = create_api_response(data={'name': 'tag1', 'url': 'http://testserver/api/tags/1/'})

        response = self.client.get('/api/tags/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/tags/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)


class QuestionTests(MockedTestCase):

    def test_list_view_empty(self):
        """ Returns an empty array when there are no results. """
        expected = create_api_response(
            data={
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            })

        response = self.client.get('/api/questions', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_list_view_non_empty(self):
        """ Returns all questions when no id is given. """
        create_question('question1')
        create_question('question2')

        expected = create_api_response(
            data={'count': 2,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'answers': [],
                       'created_on': '2020-01-01T13:00:00+13:00',
                       'description': '',
                       'is_multiple_choice': False,
                       'tags': [],
                       'text': 'question1',
                       'updated_on': '2020-01-01T13:00:00+13:00',
                       'url': 'http://testserver/api/questions/1/'},
                      {'answers': [],
                       'created_on': '2020-01-01T13:00:00+13:00',
                       'description': '',
                       'is_multiple_choice': False,
                       'tags': [],
                       'text': 'question2',
                       'updated_on': '2020-01-01T13:00:00+13:00',
                       'url': 'http://testserver/api/questions/2/'}
                  ]})

        response = self.client.get('/api/questions', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view(self):
        """ Returns the correct question when a valid id is given. """
        create_question('question1')
        create_question('question2')
        expected = create_api_response(data={'answers': [],
                                             'created_on': '2020-01-01T13:00:00+13:00',
                                             'description': '',
                                             'is_multiple_choice': False,
                                             'tags': [],
                                             'text': 'question1',
                                             'updated_on': '2020-01-01T13:00:00+13:00',
                                             'url': 'http://testserver/api/questions/1/'
                                             })

        response = self.client.get('/api/questions/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/questions/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)


class AnswerTests(MockedTestCase):
    def setUp(self) -> None:
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
                       'votes': 0},
                      {'is_correct_answer': False,
                       'question': 'http://testserver/api/questions/1/',
                       'text': 'answer',
                       'url': 'http://testserver/api/answers/2/',
                       'votes': 0}
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
                  'votes': 0})

        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)


class QuizTests(MockedTestCase):
    def setUp(self) -> None:
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

        response = self.client.get('/api/quizzes', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_list_view_non_empty(self):
        """ Returns all quizzes when no id is given. """
        create_quizzes(2)
        expected = create_api_response(
            data={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {'created_on': '2020-01-01T13:00:00+13:00',
                     'description': '',
                     'name': 'quiz_0',
                     'questions': [],
                     'updated_on': '2020-01-01T13:00:00+13:00',
                     'url': 'http://testserver/api/quizzes/1/'},
                    {'created_on': '2020-01-01T13:00:00+13:00',
                     'description': '',
                     'name': 'quiz_1',
                     'questions': [],
                     'updated_on': '2020-01-01T13:00:00+13:00',
                     'url': 'http://testserver/api/quizzes/2/'}
                ]
            })

        response = self.client.get('/api/quizzes', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view(self):
        """ Returns the correct question when a valid id is given. """
        create_quizzes(2)
        expected = create_api_response(
            data={'created_on': '2020-01-01T13:00:00+13:00',
                  'description': '',
                  'name': 'quiz_0',
                  'questions': [],
                  'updated_on': '2020-01-01T13:00:00+13:00',
                  'url': 'http://testserver/api/quizzes/1/'})

        response = self.client.get('/api/quizzes/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/quizzes/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)

# Test JWT
