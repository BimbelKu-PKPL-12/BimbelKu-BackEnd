from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from bimbelpage.models import Bimbel, User
from .serializers import SuperAdminBimbelSerializer, AdminUserSerializer
import logging

logger = logging.getLogger(__name__)

class IsSuperAdminUser(permissions.BasePermission):
    """
    Permission to only allow superadmin users to access
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'superadmin'

class SuperAdminBimbelViewSet(viewsets.ModelViewSet):
    """
    A viewset for superadmin to manage all bimbels
    """
    queryset = Bimbel.objects.all()
    serializer_class = SuperAdminBimbelSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nama', 'lokasi', 'admin__username']
    ordering_fields = ['created_at', 'nama', 'is_approved']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Superadmins can filter bimbels by approval status, admin, etc.
        """
        queryset = Bimbel.objects.all()
        
        # Filter by approval status if specified
        is_approved = self.request.query_params.get('is_approved')
        if is_approved is not None:
            is_approved_bool = is_approved.lower() == 'true'
            queryset = queryset.filter(is_approved=is_approved_bool)
        
        # Filter by admin if specified
        admin_id = self.request.query_params.get('admin_id')
        if admin_id:
            queryset = queryset.filter(admin_id=admin_id)
            
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new bimbel and handle the kuota fields
        """
        # Ensure sisa_kuota equals kuota_awal on creation
        kuota_awal = serializer.validated_data.get('kuota_awal')
        serializer.save(sisa_kuota=kuota_awal)
        logger.info(f"Superadmin created new bimbel: {serializer.instance.nama}")
    
    def perform_update(self, serializer):
        """
        Update bimbel data
        """
        # If kuota_awal changes, update sisa_kuota proportionally
        if 'kuota_awal' in serializer.validated_data:
            old_kuota = serializer.instance.kuota_awal
            new_kuota = serializer.validated_data['kuota_awal']
            
            if old_kuota != 0:  # Avoid division by zero
                ratio = serializer.instance.sisa_kuota / old_kuota
                new_sisa_kuota = int(new_kuota * ratio)
                serializer.save(sisa_kuota=new_sisa_kuota)
            else:
                serializer.save(sisa_kuota=new_kuota)
        else:
            serializer.save()
        
        logger.info(f"Superadmin updated bimbel {serializer.instance.id}: {serializer.instance.nama}")
    
    def perform_destroy(self, instance):
        """
        Delete a bimbel
        """
        bimbel_name = instance.nama
        bimbel_id = instance.id
        instance.delete()
        logger.info(f"Superadmin deleted bimbel {bimbel_id}: {bimbel_name}")
    
    @action(detail=False, methods=['get'])
    def admin_users(self, request):
        """
        Get list of admin users for assigning to bimbel
        """
        admins = User.objects.filter(role='admin')
        serializer = AdminUserSerializer(admins, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get statistics about bimbels
        """
        total_bimbels = Bimbel.objects.count()
        approved_bimbels = Bimbel.objects.filter(is_approved=True).count()
        pending_bimbels = Bimbel.objects.filter(is_approved=False).count()
        
        return Response({
            'total': total_bimbels,
            'approved': approved_bimbels,
            'pending': pending_bimbels,
        })
