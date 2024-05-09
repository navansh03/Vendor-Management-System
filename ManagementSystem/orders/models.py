from django.db import models
from django.db import models
from  django.db.models import JSONField
from vendors.models import Vendor
from django.utils import timezone

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)    
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True,blank=True)  #expected delivery date
    items = JSONField(null=True)   #details of the items ordered
    quantity = models.IntegerField() 
    #defining the choices
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)