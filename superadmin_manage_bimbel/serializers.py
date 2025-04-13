from rest_framework import serializers
from bimbelpage.models import Bimbel, User

class SuperAdminBimbelSerializer(serializers.ModelSerializer):
    admin_username = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Bimbel
        fields = [
            'id', 'nama', 'lokasi', 'kuota_awal', 'sisa_kuota',
            'deskripsi', 'harga', 'is_approved', 'created_at', 'updated_at',
            'admin', 'admin_username', 'status', 'rejection_reason'
        ]
        
    def get_admin_username(self, obj):
        return obj.admin.username if obj.admin else None
    
    def get_status(self, obj):
        return "Disetujui" if obj.is_approved else "Menunggu Persetujuan"

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['role']
