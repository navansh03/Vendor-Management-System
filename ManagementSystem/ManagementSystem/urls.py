
from django.contrib import admin
from django.urls import path, include
from vendors import urls as vendor_urls
from orders import urls as order_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(vendor_urls)),
    path("",include(order_urls)),
]
