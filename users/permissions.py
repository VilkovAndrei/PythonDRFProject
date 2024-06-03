from rest_framework.permissions import BasePermission


class UserPermissionsDestroy(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False
