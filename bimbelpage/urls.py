from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimbelViewSet

router = DefaultRouter()
router.register(r'bimbels', BimbelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bimbels/', BimbelViewSet.as_view({'get': 'list'}), name='bimbel-list'),
    path('bimbels/<int:pk>/', BimbelViewSet.as_view({'get': 'retrieve'}), name='bimbel-detail'),
    path('bimbels/create/', BimbelViewSet.as_view({'post': 'create'}), name='bimbel-create'),
]