from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsCreatorOrAdminUserOrReadOnly(BasePermission):
    """
    Allows full access if the user making the request is a admin user or the creator of the model the request is acting
    on.

    Allows read access for safe methods (GET, HEAD, OPTIONS).
    """

    USER_FIELD = 'creator'

    def has_object_permission(self, request, view, obj):
        creator = getattr(obj, self.USER_FIELD)
        return creator == request.user or request.user.is_staff or request.method in permissions.SAFE_METHODS
