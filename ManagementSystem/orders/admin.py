from django.contrib import admin
from .models import PurchaseOrder

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'order_date', 'delivery_date', 'status')
    list_filter = ('vendor', 'status')
    search_fields = ('vendor', 'status')
    list_per_page = 20


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)