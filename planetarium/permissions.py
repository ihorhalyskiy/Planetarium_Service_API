from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminAllORIsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self,request,view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user or request.user.is_staff
        elif hasattr(obj, "reservation"):
            return obj.reservation.user == request.user or request.user.is_staff
        return False
