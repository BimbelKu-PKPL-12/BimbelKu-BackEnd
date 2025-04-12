from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bimbel
from .serializers import BimbelSerializer
from .permissions import IsAdminUser, IsSiswaUser, IsOwnerOrReadOnly
from .auth_client import AuthServiceClient
import logging

logger = logging.getLogger(__name__)

class IsSuperAdminUser(permissions.BasePermission):
    """
    Permission to only allow superadmin users to access
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'superadmin'

# Custom permission that combines admin or owner or superadmin
class IsAdminOrOwnerOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is superadmin
        if hasattr(request.user, 'role') and request.user.role == 'superadmin':
            return True
        
        # Check if user is admin
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
            
        # For object-level permissions (PUT, DELETE), 
        # the has_object_permission method will be called
        return request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        # Superadmin can do anything
        if hasattr(request.user, 'role') and request.user.role == 'superadmin':
            return True
            
        # Admin access to their own bimbels
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return obj.admin == request.user
            
        # Allow read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Otherwise, only allow if the user is the owner
        return obj.admin == request.user

class BimbelViewSet(viewsets.ModelViewSet):
    queryset = Bimbel.objects.all()
    serializer_class = BimbelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOrSuperAdmin]

    def create(self, request, *args, **kwargs):
        print("In create method")
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)
        print("Has role attr:", hasattr(request.user, 'role'))
        if hasattr(request.user, 'role'):
            print("Role:", request.user.role)
        
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """
        - Admin hanya bisa melihat bimbel yang dia buat
        - SuperAdmin bisa melihat semua bimbel
        - Siswa bisa melihat semua bimbel yang disetujui
        """
        if hasattr(self.request.user, 'role') and self.request.user.role == 'superadmin':
            # SuperAdmin can see all bimbels, can filter by is_approved
            is_approved = self.request.query_params.get('is_approved')
            if is_approved is not None:
                # Convert string parameter to boolean
                is_approved_bool = is_approved.lower() == 'true'
                return Bimbel.objects.filter(is_approved=is_approved_bool)
            # If no filter, return all
            return Bimbel.objects.all()
        elif hasattr(self.request.user, 'role') and self.request.user.role == 'admin':
            return Bimbel.objects.filter(admin=self.request.user)
        elif hasattr(self.request.user, 'role') and self.request.user.role == 'siswa':
            # Siswa bisa melihat semua bimbel yang disetujui
            return Bimbel.objects.filter(is_approved=True)
        return Bimbel.objects.none()
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to better handle approval status changes
        """
        instance = self.get_object()
        logger.debug(f"Received update request for bimbel {instance.id}")
        logger.debug(f"Request data: {request.data}")
        
        # Check if this is an approval update from superadmin
        if ('is_approved' in request.data and 
            hasattr(request.user, 'role') and request.user.role == 'superadmin'):
            
            # Log the approval action
            is_approved = request.data['is_approved']
            action = "approve" if is_approved else "reject"
            logger.info(f"SuperAdmin {action}ing bimbel {instance.id}")
            
            # Partial update to only change approval status
            instance.is_approved = is_approved
            instance.save(update_fields=['is_approved', 'updated_at'])
            
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        # For normal updates, proceed with default behavior
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Override partial_update to better handle approval updates
        """
        logger.debug(f"Received PATCH request with data: {request.data}")
        return self.update(request, *args, **kwargs)
        
    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdminUser])
    def set_approval_status(self, request, pk=None):
        """
        Custom endpoint to explicitly approve or reject bimbels
        """
        bimbel = self.get_object()
        
        if 'is_approved' not in request.data:
            return Response(
                {"detail": "is_approved field is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        is_approved = request.data['is_approved']
        action = "approved" if is_approved else "rejected"
        
        # Update the bimbel instance
        bimbel.is_approved = is_approved
        bimbel.save(update_fields=['is_approved', 'updated_at'])
        
        logger.info(f"Bimbel {bimbel.id} has been {action} by {request.user.username}")
        
        return Response({
            "detail": f"Bimbel has been {action}",
            "is_approved": is_approved
        })
        
    @action(detail=False, methods=['get'])
    def my_bimbels(self, request):
        """
        Endpoint untuk Admin melihat semua bimbel yang dia buat
        """
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            bimbels = Bimbel.objects.filter(admin=request.user)
            serializer = self.get_serializer(bimbels, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "Anda tidak memiliki izin untuk melihat data ini."},
                status=status.HTTP_403_FORBIDDEN
            )


class VerifyAuthView(APIView):
    """
    View untuk memverifikasi autentikasi dan hak akses
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Verifikasi autentikasi dan kembalikan informasi user
        """
        return Response({
            'is_authenticated': request.user.is_authenticated,
            'user_id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'role': getattr(request.user, 'role', None),
            'permissions': {
                'is_admin': hasattr(request.user, 'role') and request.user.role == 'admin',
                'is_siswa': hasattr(request.user, 'role') and request.user.role == 'siswa',
            }
        })