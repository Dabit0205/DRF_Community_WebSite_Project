from rest_framework import permissions


class SignOutAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT":
            return bool(request.user and request.user.is_authenticated)
        else:
            return True
