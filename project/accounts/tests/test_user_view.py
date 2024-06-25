from accounts.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserTests(APITestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = CustomUser.objects.create_user(username='adminuser', password='adminpassword', email='adminuser@example.com', user_type='doctor', is_staff=True)
        self.admin_user.is_active = True
        self.admin_user.save()

        # Create a regular user
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com', user_type='patient')
        self.user.is_active = True
        self.user.save()

        # Get tokens for the users
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.user_token = str(RefreshToken.for_user(self.user).access_token)

        # URLs
        self.user_list_url = reverse('customuser-list')
        self.user_detail_url = lambda pk: reverse('customuser-detail', kwargs={'pk': pk})

    def test_admin_can_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'user_type': 'doctor'
        }
        response = self.client.post(self.user_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'user_type': 'doctor'
        }
        response = self.client.post(self.user_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_get_own_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.user_detail_url(self.user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_get_other_user_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.user_detail_url(self.admin_user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_user_can_delete_own_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.delete(self.user_detail_url(self.user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())

    def test_user_cannot_delete_other_user_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.delete(self.user_detail_url(self.admin_user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
