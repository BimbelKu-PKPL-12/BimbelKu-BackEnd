from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.functional import cached_property

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        
        # Tambahkan role dari token ke user object
        if 'role' in validated_token:
            # Gunakan __dict__ untuk menambahkan attribute dinamis
            user.__dict__['role'] = validated_token.get('role')
        
        return user