# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)

from orders.models import Order, PaymobOrder
from orders.views import OrderViewSet
from pharmacy.models import Pharmacy
from products.models import Category, Product

User = get_user_model()


class PaymobOrderView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.pharmacy = Pharmacy.objects.create(
            name="Test pharmacy",
            location="Test location",
            image="test_data/images/pharmacy/image.jpg",
            open_time="09:00:00",
            close_time="18:00:00",
            phone="1234567890",
        )
        self.category = Category.objects.create(name="Test category")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product 1",
            description="Test description",
            price=50.00,
            pharmacy=self.pharmacy,
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product 2",
            description="Test description",
            price=100.00,
            pharmacy=self.pharmacy,
        )

        self.factory = APIRequestFactory()
        self.client = APIClient()


        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "test_password"}
        )
        self.access_token = response.data["access"]
        self.order_data = {
            "customer": self.user.id,
            "pharmacy": self.pharmacy.id,
        }
        self.view = OrderViewSet.as_view({'get': 'retrieve'})
        self.order=self.create_order()
        # self.url = reverse('order-detail', kwargs={'pk': self.order['id']})
        self.url="/orders/paymob-order/"


    def create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post("/orders/orders/", self.order_data, format="json")
        return response.data



    @patch('orders.views.check_paymob_order_status')
    @patch('orders.views.PaymobOrder.objects.get')
    def test_retrieve_check_paid(self, mock_paymob_order_get, mock_check_paymob_order_status):
        # Create a mock PaymobOrder
        mock_paymob_order = PaymobOrder.objects.create(order_id=self.order['id'], paid=False)

        mock_paymob_order_get.return_value = mock_paymob_order

        # Mock check_paymob_order_status to return True
        mock_check_paymob_order_status.return_value = True

        request = self.factory.get(self.url)
        request.user = self.user
        force_authenticate(request, user=self.user)

        # Set query parameter to trigger check_paid condition

        response = self.client.get(f"/orders/paymob-order/?order_id={self.order['id']}&&check_paid={True}", format="json")


        # Ensure that PaymobOrder is updated to paid
        mock_paymob_order.refresh_from_db()
        self.assertTrue(mock_paymob_order.paid)

        # Ensure response is as expected
        self.assertEqual(response.status_code, 200)

    def test_retrieve_no_check_paid(self):
        # Create a mock Order
        mock_order = Order.objects.create(customer=self.user)

        request = self.factory.get(self.url)
        request.user = self.user
        force_authenticate(request, user=self.user)

        # No query parameter provided
        request.query_params = {}

        response = self.view(request, pk=mock_order.id)

        # Ensure response is as expected
        self.assertEqual(response.status_code, 200)

        # Ensure that no additional calls were made to PaymobOrder
        with self.assertRaises(PaymobOrder.DoesNotExist):
            PaymobOrder.objects.get()

    def test_retrieve_without_order_id(self):
       response = self.client.get("/orders/paymob-order/")
       self.assertEqual(response.status_code, 404)



# class PaymobOrderTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     @patch('orders.views.PaymobOrder.objects.get')
#     def test_get_existing_order(self, mock_get):
#         # Prepare mock data
#         mock_order = MagicMock()
#         order=MagicMock()
#         mock_order_data = {'order': None, 'paid': True,'amount_cents': 100, 'currency': 'EGP','paymob_order_id': '12345'}
#         mock_order.return_value = mock_order_data
#         mock_get.side_effect = mock_order

#         # Create request with query parameters
#         url = reverse('paymob-order')
#         request = self.factory.get(url, {'order_id': '12345'})

#         # Call the view
#         response = PaymobOrderView.as_view()(request)

#         # Assert that PaymobOrder.objects.get() is called with the correct parameter
#         mock_get.assert_called_once_with(order_id='12345')
#         # Assert response status code and data
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, mock_order_data)

#     @patch('orders.views.create_paymob')
#     def test_get_nonexistent_order(self, mock_create_paymob):
#         # Prepare mock data
#         mock_order_data = {'paid': True,'amount_cents': 100, 'currency': 'EGP','paymob_order_id': '12345' ,'order': None}
#         mock_create_paymob.return_value = mock_order_data
#         order_id='550e8400-e29b-41d4-a716-446655440000'
#         # Create request with query parameters
#         url = reverse('paymob-order')

#         request = self.factory.get(url, {'order_id': order_id})

#         # Call the view
#         response = PaymobOrderView.as_view()(request)

#         # Assert that create_paymob is called with the correct parameter
#         mock_create_paymob.assert_called_once_with(order_id)

#         # Assert response status code and data
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, mock_order_data)
