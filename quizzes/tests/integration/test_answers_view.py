from quizzes.tests import create_api_response, create_question, MockedTestCase, create_answer


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
                       'votes': 0,
                       'user': None},
                      {'is_correct_answer': False,
                       'question': 'http://testserver/api/questions/1/',
                       'text': 'answer',
                       'url': 'http://testserver/api/answers/2/',
                       'votes': 0,
                       'user': None}
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
                  'user': None})

        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected)

    def test_detail_view_invalid_id(self):
        """ Returns the correct response when an invalid id is specified. """
        expected = create_api_response(404, "Not Found")
        response = self.client.get('/api/answers/1', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), expected)
