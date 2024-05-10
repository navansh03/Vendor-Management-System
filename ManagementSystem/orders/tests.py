from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User



class PurchaseOrderViewSetTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name="vendor1")
        self.purchase_order = PurchaseOrder.objects.create(po_number="123", vendor=self.vendor, quantity=10, status='pending')
        self.completed_pos = PurchaseOrder.objects.create(po_number="456", vendor=self.vendor, quantity=20, status='completed')



    def test_list_purchase_orders(self):
        response = self.client.get(reverse('purchaseorders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        response = self.client.get(reverse('purchaseorders-detail', args=[self.purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_purchase_order(self):
        data = {"status": 'completed'}
        response = self.client.put(reverse('purchaseorders-detail', args=[self.purchase_order.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_purchase_order(self):
        response = self.client.delete(reverse('purchaseorders-detail', args=[self.purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
