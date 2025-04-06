# bimbelpage/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
import logging
from authapp.models import User

logger = logging.getLogger(__name__)
User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Debug
        print(f"Token payload: {validated_token}")
        
        user = super().get_user(validated_token)
        
        # Debug
        print(f"User before: {user}, ID: {user.id}, is_authenticated: {user.is_authenticated}")
        
        # Tambahkan role dari token ke user object
        if 'role' in validated_token:
            # Tambahkan role sebagai property menggunakan monkey patching
            setattr(user, 'role', validated_token.get('role'))
            print(f"Added role: {getattr(user, 'role', None)}")
        
        return user
    
    def authenticate(self, request):
        # Debug auth header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        print(f"Auth header: {auth_header}")
        
        # Lanjutkan dengan proses autentikasi normal
        result = super().authenticate(request)
        
        # Debug result
        if result:
            user, token = result
            print(f"Authenticated user: {user}, Token: {token}")
            print(f"User has role attribute: {hasattr(user, 'role')}")
            if hasattr(user, 'role'):
                print(f"User role: {user.role}")
        else:
            print("Authentication failed")
        
        return result