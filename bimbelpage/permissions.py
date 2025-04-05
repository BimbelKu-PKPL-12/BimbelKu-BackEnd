# from rest_framework import permissions

# class IsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Debug
#         print("DEBUG - User:", request.user)
#         print("DEBUG - Is authenticated:", request.user.is_authenticated)
#         print("DEBUG - Has role attr:", hasattr(request.user, 'role'))
#         if hasattr(request.user, 'role'):
#             print("DEBUG - User role:", request.user.role)
        
#         # Periksa apakah user terautentikasi dan memiliki role admin
#         return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'

# bimbelpage/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Debug
        print("DEBUG - User:", request.user)
        print("DEBUG - Auth:", request.auth)
        if hasattr(request.auth, 'payload'):
            print("DEBUG - Token payload:", request.auth.payload)
        
        # Periksa apakah user terautentikasi
        if not request.user.is_authenticated:
            return False
        
        # Periksa role dari user
        if hasattr(request.user, 'role'):
            return request.user.role == 'admin'
        
        # Alternatif: periksa langsung dari token
        if hasattr(request.auth, 'payload') and 'role' in request.auth.payload:
            return request.auth.payload['role'] == 'admin'
        
        return False