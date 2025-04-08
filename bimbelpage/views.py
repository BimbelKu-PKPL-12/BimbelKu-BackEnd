from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bimbel
from .serializers import BimbelSerializer
from .permissions import IsAdminUser, IsSiswaUser, IsOwnerOrReadOnly
from .auth_client import AuthServiceClient

class BimbelViewSet(viewsets.ModelViewSet):
    queryset = Bimbel.objects.all()
    serializer_class = BimbelSerializer
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]

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
        Admin hanya bisa melihat bimbel yang dia buat
        """
        if hasattr(self.request.user, 'role') and self.request.user.role == 'admin':
            return Bimbel.objects.filter(admin=self.request.user)
        elif hasattr(self.request.user, 'role') and self.request.user.role == 'siswa':
            # Siswa bisa melihat semua bimbel yang disetujui
            return Bimbel.objects.filter(is_approved=True)
        return Bimbel.objects.none()
    
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