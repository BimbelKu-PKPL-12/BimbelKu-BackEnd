import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class AuthServiceClient:
    """
    Client untuk berkomunikasi dengan Authentication Service
    """
    
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL
        self.auth_endpoint = f"{self.base_url}/auth"  # Disesuaikan dengan endpoint di frontend
    
    def verify_token(self, token):
        """
        Verifikasi token dengan Auth service dan dapatkan info user
        """
        try:
            response = requests.get(
                f"{self.auth_endpoint}/verify-token/",
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Token verification failed: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    def get_user_profile(self, token):
        """
        Dapatkan profil pengguna dari Auth service
        """
        try:
            response = requests.get(
                f"{self.auth_endpoint}/profile/",
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user profile: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None