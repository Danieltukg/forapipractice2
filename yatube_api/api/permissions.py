from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Изменять и удалять объект может только его автор.

    Остальным аутентифицированным пользователям объект доступен
    только для чтения. Неаутентифицированные пользователи доступа
    не получают вовсе.
    """

    message = 'Изменять и удалять чужой контент запрещено.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
