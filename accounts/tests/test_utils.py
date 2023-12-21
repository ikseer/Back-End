# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient

# User=get_user_model()
# class CorsHeadersTest(TestCase):
    
#     def setUp(self):
#         self.client = APIClient()
#         user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')

#         self.client.force_authenticate(user=user)
#     def test_cors_headers(self):


#         response = self.client.get(reverse('OTP_Gen', args=['1234567890']))
#         self.assertEqual(response.status_code, 200)
#         # print(response.headers)
#         # self.assertEqual(response['Access-Control-Allow-Origin'], '*')  # Adjust as per your CORS settings
