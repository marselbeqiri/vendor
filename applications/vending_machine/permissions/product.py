from rest_framework import permissions


class ProductPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return bool(user and user.is_authenticated and user.is_seller())
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            seller_id = obj.seller.id
            return bool(request.user and request.user.is_authenticated and request.user.id == seller_id)

        return super(ProductPermission, self).has_object_permission(request, view, obj)
