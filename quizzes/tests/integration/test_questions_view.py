from quizzes.tests import create_api_response, create_question, MockedTestCase


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
                       'url': 'http://testserver/api/questions/1/',
                       'user': None},
                      {'answers': [],
                       'created_on': '2020-01-01T13:00:00+13:00',
                       'description': '',
                       'is_multiple_choice': False,
                       'tags': [],
                       'text': 'question2',
                       'updated_on': '2020-01-01T13:00:00+13:00',
                       'url': 'http://testserver/api/questions/2/',
                       'user': None}
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
                                             'url': 'http://testserver/api/questions/1/',
                                             'user': None
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
