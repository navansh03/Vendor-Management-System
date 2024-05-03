from django.contrib import admin
from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Vendor, VendorAdmin)