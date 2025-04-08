from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimbelViewSet, VerifyAuthView

router = DefaultRouter()
router.register(r'bimbels', BimbelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-auth/', VerifyAuthView.as_view(), name='verify_auth'),
]