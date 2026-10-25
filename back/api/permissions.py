from rest_framework.permissions import BasePermission, SAFE_METHODS


def normalizar_rol(valor):
    return (valor or '').strip().lower()


def user_has_role(user, *roles):
    if not user or not user.is_authenticated:
        return False

    rol = normalizar_rol(
        getattr(getattr(user, 'id_rol', None), 'nombre_rol', '')
    )
    permitidos = {normalizar_rol(role) for role in roles}
    return rol in permitidos


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'administrador')


class IsAdminOrNutritionistRole(BasePermission):
    def has_permission(self, request, view):
        return user_has_role(
            request.user,
            'administrador',
            'nutricionista',
        )


class IsSelfOrAdminRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            user_has_role(request.user, 'administrador')
            or getattr(obj, 'id_usuario', None)
            == getattr(request.user, 'id_usuario', None)
        )


class IsAuthenticatedReadOrStaffRoleWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return user_has_role(
            request.user,
            'administrador',
            'nutricionista',
        )
