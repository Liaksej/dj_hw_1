from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Проверка владельца."""

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user == obj.creator)


class IsOwnerForFavorite(BasePermission):
    """Проверка владельца избранного."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
