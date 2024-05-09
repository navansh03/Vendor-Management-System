from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth.models import User
from .models import Vendor
from .serializers import VendorSerializer

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_vendor(name="", contact_details="", address="", vendor_code="", on_time_delivery_rate=0.0, quality_rating_avg=0.0, average_response_time=0.0, fulfillment_rate=0.0):
        if name != "" and contact_details != "" and address != "" and vendor_code != "":
            Vendor.objects.create(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code, on_time_delivery_rate=on_time_delivery_rate, quality_rating_avg=quality_rating_avg, average_response_time=average_response_time, fulfillment_rate=fulfillment_rate)

    def setUp(self):
        # add test data
        self.create_vendor("vendor1", "contact1", "address1", "code1", 1.0, 1.0, 1.0, 1.0)
        self.create_vendor("vendor2", "contact2", "address2", "code2", 2.0, 2.0, 2.0, 2.0)

        # creating a user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # create a token for the test user and providing the token in the header of the API request
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class GetAllVendorsTest(BaseViewTest):

    #various functions to test all the viewsets of the Vendor API

    def test_get_all_vendors(self):
        # hit the API endpoint
        url="http://127.0.0.1:8000/api/vendors/"
        response = self.client.get(url)
        print(url)
        expected = Vendor.objects.all() 
        serialized = VendorSerializer(expected, many=True)
        self.assertEqual(response.data,serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        # hit the API endpoint
        url = "http://127.0.0.1:8000/api/vendors/1/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_update_vendor(self):
        data = {
            "name": "updated_vendor1",
            "contact_details": "updated_contact1",
            "address": "updated_address1",
            "vendor_code": "updated_code1",
            "on_time_delivery_rate": 1.1,
            "quality_rating_avg": 1.1,
            "average_response_time": 1.1,
            "fulfillment_rate": 1.1
        }
        url = "http://127.0.0.1:8000/api/vendors/1/"
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_vendor = Vendor.objects.get(pk=1)
        self.assertEqual(updated_vendor.name, "updated_vendor1")

    
    
    def test_create_vendor(self):
        data = {
            "name": "vendor3",
            "contact_details": "contact3",
            "address": "address3",
            "vendor_code": "code3",
            "on_time_delivery_rate": 3.0,
            "quality_rating_avg": 3.0,
            "average_response_time": 3.0,
            "fulfillment_rate": 3.0
        }
        url = "http://127.0.0.1:8000/api/vendors/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)
        self.assertEqual(Vendor.objects.get(pk=3).name, "vendor3")

    
    
    def test_retrieve_vendor(self):
        url = "http://127.0.0.1:8000/api/vendors/1/"
        response = self.client.get(url)
        expected = Vendor.objects.get(pk=1)
        serialized = VendorSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
