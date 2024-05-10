
from django.contrib import admin
from django.urls import path, include,re_path
from vendors import urls as vendor_urls
from orders import urls as order_urls
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi   
from .views.py import CreateUserTokenView 


#for the API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management System APIs",
      default_version='v0.0',
      description="API documentation for this Project",
    #   terms_of_service="https://www.yourproject.com/policies/terms/",
      contact=openapi.Contact(email="navanshgoswami4@gmail.com"),
    #   license=openapi.License(name="Your Project License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    #added the swagger and redoc documentation for the API to be clear and understandable
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', CreateUserTokenView.as_view(), name='token_create'),
    path("", include(vendor_urls)),
    path("",include(order_urls)),
]
