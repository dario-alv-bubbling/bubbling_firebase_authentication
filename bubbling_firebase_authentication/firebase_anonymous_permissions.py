from rest_framework.permissions import BasePermission


class IsAuthenticatedAnonymous(BasePermission):
    """
    Allows access to authenticated anonymous users.
    """

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated)
                    or (request.user.is_anonymous and request.user.id is not None))
