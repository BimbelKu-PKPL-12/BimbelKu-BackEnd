import logging
from .auth_client import AuthServiceClient

logger = logging.getLogger(__name__)

class AuthServiceMiddleware:
    """
    Middleware untuk menyinkronkan informasi user dari Auth Service
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth_client = AuthServiceClient()
    
    def __call__(self, request):
        # Jika user sudah terautentikasi, kita bisa memperkaya data user
        if request.user.is_authenticated:
            # Dapatkan token dari header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
                # Verifikasi token dan dapatkan data terbaru
                user_data = self.auth_client.get_user_profile(token)
                
                if user_data:
                    # Update informasi user sesuai kebutuhan
                    if not hasattr(request.user, 'role'):
                        setattr(request.user, 'role', user_data.get('role'))
                    
                    logger.debug(f"User data enriched with role: {getattr(request.user, 'role', None)}")
        
        response = self.get_response(request)
        return response