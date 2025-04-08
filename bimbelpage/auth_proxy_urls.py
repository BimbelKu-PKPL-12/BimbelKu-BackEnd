from django.urls import path
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests
from django.conf import settings
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def proxy_auth_request(request, endpoint):
    """
    Proxy request ke auth service
    """
    auth_service_url = settings.AUTH_SERVICE_URL
    # Ubah URL target
    url = f"{auth_service_url}/api/auth/{endpoint}/"
    
    print(f"Forwarding request to: {url}")
    
    try:
        # Convert request data to json
        data = request.data
        
        # Forward request ke auth service
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Auth service response status: {response.status_code}")
        
        # Return response dari auth service
        return JsonResponse(
            response.json(), 
            status=response.status_code,
            safe=False
        )
    except Exception as e:
        print(f"Error forwarding to auth service: {str(e)}")
        return JsonResponse(
            {'error': f'Failed to connect to auth service: {str(e)}'},
            status=500
        )

urlpatterns = [
    path('login/', proxy_auth_request, {'endpoint': 'login'}, name='proxy_login'),
    path('register/', proxy_auth_request, {'endpoint': 'register'}, name='proxy_register'),
    path('token/refresh/', proxy_auth_request, {'endpoint': 'token/refresh'}, name='proxy_refresh'),
]