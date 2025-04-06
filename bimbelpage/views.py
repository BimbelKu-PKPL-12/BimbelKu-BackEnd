from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bimbel
from .serializers import BimbelSerializer
from .permissions import IsAdminUser

class BimbelViewSet(viewsets.ModelViewSet):
    queryset = Bimbel.objects.all()
    serializer_class = BimbelSerializer
    # permission_classes = [IsAdminUser]
    permission_classes = [permissions.IsAuthenticated]

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
        return Bimbel.objects.filter(admin=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_bimbels(self, request):
        """
        Endpoint untuk Admin melihat semua bimbel yang dia buat
        """
        bimbels = Bimbel.objects.filter(admin=request.user)
        serializer = self.get_serializer(bimbels, many=True)
        return Response(serializer.data)