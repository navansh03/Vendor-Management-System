from django.shortcuts import render
from .serializers import PurchaseOrderSerializer
from .models import PurchaseOrder
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from vendors.models import Vendor, VendorPerformance
from django.db.models import F, Avg
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class PurchaseOrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    #to filter out the purchase order with an optiom to vendor ac to the vendor_id
    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id is not None:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset
    


    def create(self, request, *args, **kwargs):
        po_number = request.data.get('po_number')
        if PurchaseOrder.objects.filter(po_number=po_number).exists():
            return Response({"error": "Purchase Order with this purchase order number already exists. There is some error at your side plz check"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)  
        except:
            return Response({"error": "Purchase Order with this po_id does not exist"}, status=status.HTTP_404_NOT_FOUND) 


    #This endpoint will update acknowledgment_date and trigger the recalculation of average_response_time.  
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()        
        po.save()
        serializer = self.get_serializer(po, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response({"success": "Acknowledgment date added successfully"}, status=status.HTTP_200_OK)

    #it is called when something in the purchase order is changed
    def perform_update(self, serializer):
        po = self.get_object()
        serializer.save()
        vendor = Vendor.objects.get(id=po.vendor_id)
        total_pos= PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()

        #for the fullfillment rate for anychange in PO status
        if total_pos>0:
            vendor.fulfillment_rate = fulfilled_pos / total_pos

        if po.status == 'completed':
           
            completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
            on_time_pos = completed_pos.filter(delivery_date__lte=F('order_date')).count()
            total_completed_pos = completed_pos.count()

            if total_completed_pos > 0:
                vendor.on_time_delivery_rate = on_time_pos / total_completed_pos


            #it will save the instances of the vendor performance which will be used to view the performance trends of the vendor
            VendorPerformance.objects.create(
                vendor=vendor,
                date=timezone.now(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_average,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            )

        if po.quality_rating is not None:
            quality_rating_average = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
            vendor.quality_rating_average = quality_rating_average

        if po.acknowledgment_date is not None:
            avg_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(avg_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time']
            vendor.average_response_time = avg_response_time

        vendor.save()


    
    def update(self, request, pk=None, *args, **kwargs):
        po = self.get_object()
        serializer = self.get_serializer(po, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"success":"Successfully!! Updated the data you can see it! ","data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, pk=None, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({"success": "PurchaseOrder deleted successfully"}, status=status.HTTP_204_NO_CONTENT)