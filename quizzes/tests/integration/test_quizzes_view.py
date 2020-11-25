from quizzes.tests import create_api_response, create_question, MockedTestCase, create_quizzes


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
                     'url': 'http://testserver/api/quizzes/1/',
                     'creator': None},
                    {'created_on': '2020-01-01T13:00:00+13:00',
                     'description': '',
                     'name': 'quiz_1',
                     'questions': [],
                     'updated_on': '2020-01-01T13:00:00+13:00',
                     'url': 'http://testserver/api/quizzes/2/',
                     'creator': None}
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
                  'url': 'http://testserver/api/quizzes/1/',
                  'creator': None})

        response = self.client.get('/api/quizzes/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/quizzes/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)
