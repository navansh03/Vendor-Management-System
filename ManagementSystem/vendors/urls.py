from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet


#due to using of viewsets functions in views.py, we need to use DefaultRouter
router = DefaultRouter()
router.register(r'api/vendors', VendorViewSet, basename='vendor')

urlpatterns = [
    path('', include(router.urls)),
]