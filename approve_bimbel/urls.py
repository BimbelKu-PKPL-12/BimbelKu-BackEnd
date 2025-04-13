from django.urls import path
from .views import PendingBimbelView, BimbelApprovalView

app_name = 'approve_bimbel'

urlpatterns = [
    path('pending/', PendingBimbelView.as_view(), name='pending-bimbels'),
    path('<int:bimbel_id>/approve/', BimbelApprovalView.as_view(), name='bimbel-approval'),
]