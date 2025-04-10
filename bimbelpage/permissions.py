# bimbelpage/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission untuk memeriksa apakah user memiliki role admin
    """
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

class IsSiswaUser(permissions.BasePermission):
    """
    Permission untuk memeriksa apakah user memiliki role siswa
    """
    def has_permission(self, request, view):
        # Periksa apakah user terautentikasi dan memiliki role siswa
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'siswa'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission untuk memastikan hanya pemilik yang dapat mengedit objek
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions diizinkan untuk request GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Periksa apakah objek memiliki field admin dan user adalah admin
        admin_field = getattr(obj, 'admin', None)
        if admin_field:
            return obj.admin == request.user
        
        # Fallback ke pemeriksaan standar owner
        return obj.owner == request.user