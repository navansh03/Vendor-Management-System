from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet


#due to using of viewsets functions in views.py, we need to use DefaultRouter
router = DefaultRouter()
router.register(r'api/purchase_order',PurchaseOrderViewSet , basename='purchaseorders')

urlpatterns = [
    path('', include(router.urls)),
]