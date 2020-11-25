from rest_framework.viewsets import ModelViewSet

from quizzes.mixins import CreateUserLinkedModelMixin


class UserLinkedModelViewSet(CreateUserLinkedModelMixin, ModelViewSet):
    """
    ModelViewSet that sets the user related to an object being created to the user who made the request.

    See CreateUserLinkedModelMixin for details.
    """
    pass
