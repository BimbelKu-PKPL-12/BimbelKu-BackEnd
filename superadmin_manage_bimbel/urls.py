from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuperAdminBimbelViewSet

router = DefaultRouter()
router.register(r'bimbels', SuperAdminBimbelViewSet)

app_name = 'superadmin_manage_bimbel'

urlpatterns = [
    path('', include(router.urls)),
]
