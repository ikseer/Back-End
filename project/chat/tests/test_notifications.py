from chat.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User=get_user_model()

class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = FCMToken.objects.create(user=self.user, token='fake_token')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        self.conservation.users.add(self.user)

    def test_send_notification_on_new_message(self):
        url = reverse('message-list')
        data = {'conservation': self.conservation.id, 'text': 'A test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ensure that notification sending is logged or check side effects

    def test_update_fcm_token(self):
        url = reverse('fcm-token-list')
        self.user2 = User.objects.create_user(username='test', password='testpassword')
        data = {'user':self.user2.id,'token': 'new_fake_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user2.fcm_token.token, 'new_fake_token')
