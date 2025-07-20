from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Admin rolüne sahip kullanıcılar için izin.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin' 