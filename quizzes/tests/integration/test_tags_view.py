from django.test import TestCase

from quizzes.tests import create_api_response, create_tag


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
