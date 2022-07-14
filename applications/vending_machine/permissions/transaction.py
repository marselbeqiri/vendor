from rest_framework import permissions


class TransactionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action in ['create', 'list', 'state', 'reset']:
            return bool(user and user.is_authenticated and user.is_buyer())
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'state']:
            user_id = obj.user_id
            return bool(request.user and request.user.is_authenticated and request.user.id == user_id)

        return super(TransactionPermission, self).has_object_permission(request, view, obj)
