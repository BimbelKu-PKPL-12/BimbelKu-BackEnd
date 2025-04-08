# bimbelpage/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from bimbelpage.models import User

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Implementasi custom untuk mendapatkan user dari token yang valid.
        Jika user ada di database lokal, gunakan user tersebut.
        Jika tidak, buat user baru berdasarkan informasi dari token.
        """
        user_id = validated_token.get('user_id')
        if not user_id:
            return AnonymousUser()
        
        # Cari atau buat user lokal berdasarkan user_id dari token
        try:
            # Coba dapatkan user lokal
            user = User.objects.get(id=user_id)
            
            # Update informasi user dari token jika perlu
            if validated_token.get('username'):
                user.username = validated_token.get('username')
            if validated_token.get('email'):
                user.email = validated_token.get('email')
            
            # Tambahkan role dari token
            if 'role' in validated_token:
                setattr(user, 'role', validated_token.get('role'))
                
            user.save()
            
        except User.DoesNotExist:
            # Jika user tidak ada, buat user baru
            user = User.objects.create(
                id=user_id,
                username=validated_token.get('username', f'user_{user_id}'),
                email=validated_token.get('email', f'user_{user_id}@example.com')
            )
            # Tambahkan role dari token
            if 'role' in validated_token:
                setattr(user, 'role', validated_token.get('role'))
            
        return user
    
    def authenticate(self, request):
        """
        Proses autentikasi dengan penanganan khusus untuk token dari
        authentication service terpisah
        """
        # Debug auth header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        logger.debug(f"Auth header: {auth_header}")
        
        # Lanjutkan dengan proses autentikasi normal
        result = super().authenticate(request)
        
        # Debug result
        if result:
            user, token = result
            logger.debug(f"Authenticated user: {user}, Token: {token}")
            logger.debug(f"User has role attribute: {hasattr(user, 'role')}")
            if hasattr(user, 'role'):
                logger.debug(f"User role: {user.role}")
        else:
            logger.debug("Authentication failed")
        
        return result