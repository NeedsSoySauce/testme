from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class CreateUserLinkedModelMixin(CreateModelMixin, GenericViewSet):
    """
    Set the user related to an object being created to the user who made the request.

    Usage:
        Override the class and set the `.queryset` and `.serializer_class` attributes. Make sure to call the super
        'perform_create' method if you override it. Set the USER_FIELD class attribute to the name of the model's user
        field (default is 'creator').
    """
    USER_FIELD = 'creator'

    def perform_create(self, serializer):
        save_kwargs = {}

        if not self.request.user.is_anonymous:
            save_kwargs[self.USER_FIELD] = self.request.user

        serializer.save(**save_kwargs)
