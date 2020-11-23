from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class DescriptiveJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None, message=None):
        response: Response = renderer_context['response']

        wrapped_data = {
            'status': response.status_code,
            'success': response.status_code < 400,
            'message': message or response.status_text,
            'data': data
        }

        return super().render(wrapped_data, accepted_media_type, renderer_context)
