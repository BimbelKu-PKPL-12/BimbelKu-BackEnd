from rest_framework import serializers
from bimbelpage.models import Bimbel

class BimbelApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer for handling bimbel approval/rejection
    """
    # Accept both snake_case and camelCase field names
    is_approved = serializers.BooleanField(required=False)
    isApproved = serializers.BooleanField(required=False)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    rejectionReason = serializers.CharField(required=False, allow_blank=True, source='rejection_reason')
    
    class Meta:
        model = Bimbel
        fields = ['is_approved', 'isApproved', 'rejection_reason', 'rejectionReason']
    
    def validate(self, data):
        """
        Ensure either is_approved or isApproved is provided
        and normalize them to the field name used by the model
        """
        # If camelCase field provided, copy to snake_case field
        if 'isApproved' in data and 'is_approved' not in data:
            data['is_approved'] = data['isApproved']
            
        # We need at least one approval field
        if 'is_approved' not in data:
            raise serializers.ValidationError("Either 'is_approved' or 'isApproved' field is required")
            
        return data

class PendingBimbelSerializer(serializers.ModelSerializer):
    """
    Serializer for listing pending bimbels
    """
    admin_username = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Bimbel
        fields = [
            'id', 'nama', 'lokasi', 'kuota_awal', 'sisa_kuota',
            'deskripsi', 'harga', 'is_approved', 'created_at',
            'admin', 'admin_username', 'status', 'rejection_reason'
        ]
    
    def get_admin_username(self, obj):
        return obj.admin.username if obj.admin else None
    
    def get_status(self, obj):
        return "Disetujui" if obj.is_approved else "Menunggu Persetujuan"
