from rest_framework import serializers
from .models import Bimbel

class BimbelSerializer(serializers.ModelSerializer):
    admin_username = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Bimbel
        fields = [
            'id', 'nama', 'lokasi', 'kuota_awal', 'sisa_kuota',
            'deskripsi', 'harga', 'is_approved', 'created_at',
            'admin', 'admin_username', 'status'
        ]
        read_only_fields = ['admin', 'created_at', 'is_approved']
    
    def get_admin_username(self, obj):
        return obj.admin.username if obj.admin else None
    
    def get_status(self, obj):
        return "Disetujui" if obj.is_approved else "Menunggu Persetujuan"
    
    def create(self, validated_data):
        # Set sisa_kuota sama dengan kuota_awal saat pembuatan
        validated_data['sisa_kuota'] = validated_data['kuota_awal']
        # Set admin dari request user
        validated_data['admin'] = self.context['request'].user
        return super().create(validated_data)