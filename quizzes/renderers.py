from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class QuizzesJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: Response = renderer_context['response']

        is_ok = response.status_code < 400

        wrapped_data = {
            'status': response.status_code,
            'success': is_ok,
            'message': response.status_text
        }

        if is_ok:
            wrapped_data['data'] = data

        return super().render(wrapped_data, accepted_media_type, renderer_context)
