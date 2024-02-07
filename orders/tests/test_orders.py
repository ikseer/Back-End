from unicodedata import category
from django.test import TestCase
from orders.models import *
from products.models import *
from orders.serializers import OrderSerializer, OrderItemSerializer
from django.contrib.auth import get_user_model
from pharmacy.models import *
from django.urls import reverse
from rest_framework import status
User=get_user_model()
from rest_framework.test import APIClient



class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.pharmacy = Pharmacy.objects.create(name='Test pharmacy', location='Test location', image='test_data/images/pharmacy/image.jpg', open_time='09:00:00', close_time='18:00:00', phone='1234567890') 
        self.category = Category.objects.create(name='Test category')
        self.product1 = Product.objects.create(category=self.category, name='Product 1', description='Test description', price=50.00, pharmacy=self.pharmacy)
        self.product2 = Product.objects.create(category=self.category, name='Product 2', description='Test description', price=100.00, pharmacy=self.pharmacy)

        self.client = APIClient()
        url = reverse('rest_login')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'test_password'})
        self.access_token = response.data['access']
        self.order_data = {
            'customer': self.user.id,
            'pharmacy': self.pharmacy.id,
        }
        
    def create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post('/orders/orders/', self.order_data, format='json')
        return response.data
    def create_order_item(self):
        order=self.create_order()
        order_item={
            'product': self.product1.id,
            'quantity': 2,
            'order': int(order['id']),
        }
        response = self.client.post('/orders/orderItem/', order_item, format='json')
        return response.data
    
    #--------------------------------------
    def test_create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post('/orders/orders/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        order=self.create_order()
        response = self.client.put('/orders/orders/'+str(order['id'])+'/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        order=self.create_order()
        response = self.client.delete('/orders/orders/'+str(order['id'])+'/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.create_order()
        response = self.client.get('/orders/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #---------------------------------------------------------------
        
    def test_create_order_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        order=self.create_order()
        order_item={
            'product': self.product1.id,
            'quantity': 2,
            'order': int(order['id']),
        }
        response = self.client.post('/orders/orderItem/', order_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        order_item=self.create_order_item()
        order_item_data={
            'product': self.product1.id,
            'quantity': 2,
            'order': int(order_item['order']),
        }
        response = self.client.put('/orders/orderItem/'+str(order_item['id'])+'/', order_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        order_item=self.create_order_item()
        response = self.client.delete('/orders/orderItem/'+str(order_item['id'])+'/', order_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_get_order_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.create_order_item()
        response = self.client.get('/orders/orderItem/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

