from rest_framework import permissions


class IsSelfOrAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows full access if the user making the request is a admin user or the user making the request is the same as the
    user model the request is acting on.

    Allows read access for safe methods (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff or request.method in permissions.SAFE_METHODS
