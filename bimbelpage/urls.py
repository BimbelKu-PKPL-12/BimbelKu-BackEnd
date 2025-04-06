from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimbelViewSet

router = DefaultRouter()
router.register(r'bimbels', BimbelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]