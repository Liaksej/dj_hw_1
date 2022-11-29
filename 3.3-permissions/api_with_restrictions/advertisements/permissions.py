from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверка владельца."""

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            return request.user == obj.creator
        return request.user == obj.user


class IsOwnerForFavorite(BasePermission):
    """Проверка владельца избранного."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
