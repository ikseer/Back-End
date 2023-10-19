from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  # Import default_token_generator

User = get_user_model()

class DjRestAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'test',
            'password': 'testpassword',
            'password': 'testpassword',
            'first_name': 'first_test_name',
            'last_name': 'last_test_name',
            'email': 'test@example.com',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        self.uid = force_bytes(urlsafe_base64_decode(uid))
    def test_user_registration_view(self):
        url = reverse('rest_register')
        user_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_view(self):
        user_data = {
            'password': 'testpassword',
            'email': 'test@example.com',
        }
        url = reverse('rest_login')
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_view(self):
        url = reverse('rest_logout')  
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_password_change_view(self):
        url = reverse('rest_password_change')  # Replace with the URL name for your password change view

        data = {
            'old_password': 'testpassword',  # Current password
            'new_password1': 'newpassword123',  # New password
            'new_password2': 'newpassword123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_view(self):
        data = {'email': self.user_data['email']}
        url = reverse('rest_password_reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_password_reset_confirm_view(self):
        # Generate the UID
        # uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        # Generate the token
        # token = default_token_generator.make_token(self.user)

        reset_url = reverse('rest_password_reset_confirm')
        data = {
            'uid': self.uid,
            'token': self.token,
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }

        response = self.client.post(reset_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_password_reset_confirm_view(self):
    #     uid = urlsafe_base64_encode(force_bytes(self.user.pk))
    #     token = default_token_generator.make_token(self.user)
      
    #     reset_url = reverse('rest_password_reset_confirm')
    #     data = {
    #         'uid': uid,
    #         'token': token,
    #         'new_password1': 'newpassword123',
    #         'new_password2': 'newpassword123'
    #     }

    #     response = self.client.post(reset_url, data, format='json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_password_reset_token(self):
    #     url = reverse('rest_password_reset')
    #     self.client.post(url, self.client_data, format='json')




    # def test_password_reset_confirm_view(self):
    #     reset_url = reverse('rest_password_reset')
    #     reset_data = {'email': 'test@example.com'}
    #     reset_response = self.client.post(reset_url, reset_data, format='json')
    #     self.assertEqual(reset_response.status_code, status.HTTP_200_OK)
    #     uid = reset_response.data['uid']
    #     token = reset_response.data['key']
        
    #     confirm_url = reverse('rest_password_reset_confirm')
    #     confirm_data = {
    #         'uid': uid,
    #         'token': token,
    #         'new_password1': 'newpassword',
    #         'new_password2': 'newpassword',
    #     }
    #     confirm_response = self.client.post(confirm_url, confirm_data, format='json')
    #     self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)
    
   

    # def test_user_profile_view(self):
    #     url = reverse('rest_user_details')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_user_profile_update_view(self):
    #     url = reverse('rest_user_details')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     data = {
    #         'username': 'updated_username',
    #         'email': 'updated_email@example.com',
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
