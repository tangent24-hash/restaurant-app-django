from rest_framework.permissions import BasePermission, SAFE_METHODS


class EditPermission(BasePermission):
    """
    Allows staff users to edit any order and owners to edit their own orders.
    """

    def has_permission(self, request, view):
        # Allow access for GET, HEAD, and OPTIONS requests for everyone
        if request.method in SAFE_METHODS:
            return True

        # For editing (PUT, PATCH, DELETE), check user type
        return (
            request.user.is_staff or request.user.has_perm("myapp.editing_access"))

