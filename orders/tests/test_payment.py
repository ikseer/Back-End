# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)

from orders.models import Order, PaymobOrder
from orders.utils import check_paymob_order_status
from orders.views import OrderViewSet, PaymobCallbackViewSet
from pharmacy.models import Pharmacy
from products.models import Category, Product

User = get_user_model()

class PaymobCallbackViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PaymobCallbackViewSet.as_view()
        self.url = reverse('paymob-callback')
        # Mocking config value
        self.mock_incoming_hmac = 'your_mocked_incoming_hmac'

    @patch('orders.views.AcceptCallback')
    @patch('orders.views.PaymobOrder.objects.get')
    def test_post_success(self, mock_paymob_order_get, mock_accept_callback):
        request_data = {'key': 'value'}  # Add your request data here
        request = self.factory.post(self.url, request_data)
        request.data = request_data
        request.user = None  # or set user if authentication is needed
        request.content_type = 'application/json'
        force_authenticate(request, user=None)  # Adjust authentication if needed

        # Mocking AcceptCallback object
        mock_callback_instance = mock_accept_callback.return_value
        mock_callback_instance.is_valid = True
        mock_callback_instance.obj.order.paid_amount_cents = 1000  # Adjust values as needed
        mock_callback_instance.obj.order.amount_cents = 1000  # Adjust values as needed

        # Mocking PaymobOrder object
        mock_paymob_order = mock_paymob_order_get.return_value
        mock_paymob_order.paid = False

        response = self.view(request)

        # Ensure the PaymobOrder is marked as paid
        mock_paymob_order_get.assert_called_once()
        mock_paymob_order.save.assert_called_once_with()

        # Ensure response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_paymob_order.paid, True)
        self.assertEqual(response.data, {"success": True})


    @patch('orders.views.AcceptCallback')
    def test_post_failure(self, mock_accept_callback):
        request_data = {'key': 'value'}  # Add your request data here
        request = self.factory.post(self.url, request_data)
        request.data = request_data
        request.user = None  # or set user if authentication is needed
        request.content_type = 'application/json'
        force_authenticate(request, user=None)  # Adjust authentication if needed

        # Mocking AcceptCallback object
        mock_callback_instance = mock_accept_callback.return_value
        mock_callback_instance.is_valid = False

        response = self.view(request)

        # Ensure response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"success": False})


    @patch('orders.views.AcceptCallback')
    @patch('orders.views.PaymobOrder.objects.get')
    def test_post_fail(self, mock_paymob_order_get, mock_accept_callback):
        request_data = {'key': 'value'}  # Add your request data here
        request = self.factory.post(self.url, request_data)
        request.data = request_data
        request.user = None  # or set user if authentication is needed
        request.content_type = 'application/json'
        force_authenticate(request, user=None)  # Adjust authentication if needed

        # Mocking AcceptCallback object
        mock_callback_instance = mock_accept_callback.return_value
        mock_callback_instance.is_valid = False
        mock_callback_instance.obj.order.paid_amount_cents = 1000  # Adjust values as needed
        mock_callback_instance.obj.order.amount_cents = 1000  # Adjust values as needed

        # Mocking PaymobOrder object
        mock_paymob_order = mock_paymob_order_get.return_value
        mock_paymob_order.paid = False

        response = self.view(request)

        # Ensure the PaymobOrder is marked as paid
        # mock_paymob_order_get.assert_called_once()
        # mock_paymob_order.save.assert_called_once_with()

        self.assertEqual(mock_paymob_order.paid, False)
        self.assertEqual(response.data, {"success": False})



class OrderTest(TestCase):
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
        self.url = reverse('order-detail', kwargs={'pk': self.order['id']})

    def create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post("/orders/orders/", self.order_data, format="json")
        return response.data

#     def test_get_orders(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         order=self.create_order()
#         response = self.client.get(f"/orders/orders/{order['id']}/?check_paid={True}", format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


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

        response = self.client.get(f"/orders/orders/{self.order['id']}/?check_paid={True}", format="json")


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



class TestCheckPaymobOrderStatus(TestCase):
    def SetUp(self):
        pass

    @patch('orders.utils.PaymobOrder.objects.get')
    @patch('orders.utils.accept_api_client.get_order')
    def test_check_paymob_order_status(self, mock_get_order, mock_paymob_order_get):
        # Mocking PaymobOrder existence
        mock_paymob_order_get.side_effect = lambda **kwargs: MagicMock(amount_cents=1000)

        # Mocking accept_api_client response
        mock_get_order.return_value = (200, MagicMock(amount_cents=800), "Success")

        # Test with a valid Paymob Order ID
        result = check_paymob_order_status("valid_paymob_order_id")
        self.assertTrue(result)

        # Test with a nonexistent Paymob Order ID
        mock_paymob_order_get.side_effect = PaymobOrder.DoesNotExist
        result = check_paymob_order_status("nonexistent_paymob_order_id")
        self.assertFalse(result)

        # Test with a Paymob Order ID where amount_cents is less than response_order amount_cents
        mock_paymob_order_get.side_effect = lambda **kwargs: MagicMock(amount_cents=500)
        result = check_paymob_order_status("valid_paymob_order_id")
        self.assertFalse(result)
