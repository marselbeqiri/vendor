from rest_framework.permissions import BasePermission


class CanBuyProduct(BasePermission):
    """
    Allows access only to Buyer Role users.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if not user.is_buyer():
            return False
        return bool(user and request.user.is_authenticated)
