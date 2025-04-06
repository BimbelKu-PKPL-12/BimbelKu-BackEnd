# bimbelpage/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Debug
        print("DEBUG - User:", request.user)
        print("DEBUG - Is authenticated:", request.user.is_authenticated)
        print("DEBUG - Has role attr:", hasattr(request.user, 'role'))
        if hasattr(request.user, 'role'):
            print("DEBUG - User role:", request.user.role)
        else:
            print("DEBUG - User has no role attribute")
        
        # Periksa apakah user terautentikasi dan memiliki role admin
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'