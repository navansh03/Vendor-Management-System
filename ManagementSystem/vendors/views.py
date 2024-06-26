from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class VendorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.avg_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    

    def create(self, request, *args, **kwargs):
        vendor_code = request.data.get('vendor_code')
        if Vendor.objects.filter(vendor_code=vendor_code).exists():
            return Response({"error": "Vendor with this vendor code already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except:
            return Response({"error": "Vendor with the provided id doesn't exist."}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully!! Updated the data you can see it! ","data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None, *args, **kwargs):
        vendor = self.get_object()
        vendor.delete()
        return Response({"success": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)