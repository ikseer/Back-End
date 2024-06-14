

from django.contrib.auth import get_user_model

User = get_user_model()

# class PaymobCallbackViewSetTest(TestCase):

#     def setUp(self):
#           pass
#     @patch('orders.utils.calculate_amount_cents')
#     @patch('orders.views.PaymobOrder.objects.get')
#     def test_post_success(self, mock_paymob_order_get,calc):

#         # Mocking PaymobOrder object
#         mock_paymob_order = mock_paymob_order_get.return_value
#         calc.return_value=100
#         create_paymob(78)
