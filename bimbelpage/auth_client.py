import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class AuthServiceClient:
    """
    Client for interacting with the authentication service
    """
    
    def __init__(self):
        self.auth_service_url = settings.AUTH_SERVICE_URL
    
    def get_user_profile(self, token):
        """
        Get user profile information from the auth service using the provided token
        
        Args:
            token (str): JWT access token
            
        Returns:
            dict: User profile data or None if request failed
        """
        try:
            logger.debug(f"Requesting user profile from auth service")
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Try to get user data from authentication service
            response = requests.get(
                f"{self.auth_service_url}/api/auth/user/",
                headers=headers,
                timeout=5  # Add timeout to prevent hanging
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.debug(f"Successfully retrieved user data: {user_data}")
                return user_data
            else:
                logger.warning(f"Failed to get user data. Status code: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            # Handle connection errors gracefully
            logger.error(f"Error connecting to auth service: {str(e)}")
            return None
        except Exception as e:
            # Catch any other exceptions
            logger.error(f"Unexpected error when getting user profile: {str(e)}")
            return None
    
    def verify_token(self, token):
        """
        Verify if a token is valid with the auth service
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.auth_service_url}/api/auth/token/verify/",
                json={'token': token},
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return False
