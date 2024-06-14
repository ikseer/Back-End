
import uuid
from unittest.mock import MagicMock, Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import PaymobOrder
from orders.utils import check_paymob_order_status, create_paymob
from orders.views import PaymobCallbackViewSet
from rest_framework.test import APIRequestFactory, force_authenticate

User = get_user_model()

class PaymobCallbackViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PaymobCallbackViewSet.as_view()
        self.url = reverse('paymob-callback')
        # Mocking config value
        self.mock_incoming_hmac = 'your_mocked_incoming_hmac'

    @patch('orders.views.paymob.AcceptCallback')
    @patch('orders.views.paymob.PaymobOrder.objects.get')
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


    @patch('orders.views.paymob.AcceptCallback')
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


    @patch('orders.views.paymob.AcceptCallback')
    @patch('orders.views.paymob.PaymobOrder.objects.get')
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

class TestCheckPaymobOrderStatus(TestCase):
    def SetUp(self):
        pass

    @patch('orders.utils.PaymobOrder.objects.get')
    @patch('paymob.accept.AcceptAPIClient.get_order')
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

class TestCreatePaymob(TestCase):

    def setUp(self):
        self.order_id =uuid.uuid4()
    @patch('paymob.accept.AcceptAPIClient.create_order')
    @patch('orders.utils.calculate_product_price')
    @patch('paymob.accept.utils.AcceptUtils.generate_merchant_order_id')
    @patch('orders.models.PaymobOrder.objects.create')
    @patch('orders.models.Order.objects.get')
    @patch('orders.models.OrderItem.objects.filter')
    def test_create_paymob_success(self, mock_order_item_filter, mock_order_get, mock_paymob_create, mock_generate_merchant_order_id, mock_calculate_product_price, mock_accept_api_client_instance):
        # Mocking database objects
        lst = []
        for _ in range(3):
            order_item = Mock()
            lst.append(order_item)

        mock_order_item_filter.return_value = lst
        mock_calculate_product_price.return_value = 100

        mock_accept_api_client_instance.return_value = (10, Mock(id=1), "Feedback")


        # Mocking API client response
        # mock_accept_api_client_instance=Mock()
        # mock_accept_api_client_instance.create_order.return_value = (200, Mock(id=1), "Feedback")

        # Mocking generate_merchant_order_id
        mock_generate_merchant_order_id.return_value = "merchant_order_id"
        paymob={
            "order_id": self.order_id,
            "paymob_order_id": 1,
            "amount_cents": 300
        }
        mock_paymob_create.return_value = Mock(**paymob)
        mock_order_get.return_value = Mock(id=1)

        # Calling the function

        result = create_paymob(self.order_id)

        # Assertions
        # self.assertIsInstance(result, PaymobOrder)
        self.assertEqual(result.order_id, self.order_id)
        mock_paymob_create.assert_called_once_with(order_id=self.order_id, paymob_order_id=1, amount_cents=300)
        mock_accept_api_client_instance.assert_called_once_with(
            merchant_order_id="merchant_order_id",
            amount_cents=300,
            currency="EGP"
        )
