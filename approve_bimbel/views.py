from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from bimbelpage.models import Bimbel
from .serializers import BimbelApprovalSerializer, PendingBimbelSerializer
import logging

logger = logging.getLogger(__name__)

class IsSuperAdminUser(permissions.BasePermission):
    """
    Permission to only allow superadmin users to access
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'superadmin'

class PendingBimbelView(APIView):
    """
    View to list all pending bimbels
    """
    permission_classes = [permissions.IsAuthenticated, IsSuperAdminUser]
    
    def get(self, request):
        """Get all pending bimbel registrations"""
        try:
            # Since we're in a single backend, we can directly query the model
            pending_bimbels = Bimbel.objects.filter(is_approved=False)
            serializer = PendingBimbelSerializer(pending_bimbels, many=True)
            
            # Log for audit purposes
            logger.info(f"Super admin viewed pending bimbels. Count: {len(pending_bimbels)}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error retrieving pending bimbels: {str(e)}")
            return Response(
                {"error": "An error occurred while retrieving pending bimbels"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BimbelApprovalView(APIView):
    """
    View to approve or reject bimbels
    """
    permission_classes = [permissions.IsAuthenticated, IsSuperAdminUser]
    
    def patch(self, request, bimbel_id):
        """Approve or reject a bimbel registration"""
        try:
            # Get the bimbel instance
            try:
                bimbel = Bimbel.objects.get(id=bimbel_id)
            except Bimbel.DoesNotExist:
                return Response(
                    {"error": f"Bimbel with ID {bimbel_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            logger.debug(f"Received approval data: {request.data}")
            serializer = BimbelApprovalSerializer(data=request.data)
            
            if serializer.is_valid():
                # Update the approval status - make sure it's not None
                is_approved = serializer.validated_data.get('is_approved')
                if is_approved is None:
                    return Response(
                        {"error": "Approval status cannot be null"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                bimbel.is_approved = is_approved
                
                # Store rejection reason if provided
                if not is_approved and serializer.validated_data.get('rejection_reason'):
                    bimbel.rejection_reason = serializer.validated_data.get('rejection_reason')
                
                bimbel.save()
                
                # Log for audit purposes
                action = "approved" if bimbel.is_approved else "rejected"
                logger.info(f"Super admin {action} bimbel ID {bimbel_id}")
                
                return Response({
                    "message": f"Bimbel successfully {action}",
                    "is_approved": bimbel.is_approved
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error approving/rejecting bimbel: {str(e)}", exc_info=True)
            return Response(
                {"error": "An error occurred during approval process"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )