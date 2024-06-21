# myapp/tests.py
from chat.models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class MessageTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        self.conservation.users.add(self.user)

    def test_create_message(self):
        url = reverse('message-list')
        data = {'conservation': self.conservation.id, 'text': 'A test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'A test message')
        self.assertEqual(Message.objects.get().sender, self.user)

    def test_list_messages(self):
        Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message 1')
        Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message 2')
        url = reverse('message-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_message_detail(self):
        message = Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message')
        url = reverse('message-detail', kwargs={'pk': message.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Test message')
        self.assertEqual(response.data['sender']['username'], 'testuser')

    def test_update_message(self):
        message = Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message')
        url = reverse('message-detail', kwargs={'pk': message.id})
        updated_data = {'text': 'Updated message'}
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.text, 'Updated message')

    def test_delete_message(self):
        message = Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message')
        url = reverse('message-detail', kwargs={'pk': message.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)

    def test_message_conservation_relationship(self):
        message = Message.objects.create(conservation=self.conservation, sender=self.user, text='Test message')
        url = reverse('message-detail', kwargs={'pk': message.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['conservation'], self.conservation.id)

    def test_message_invalid_data(self):
        url = reverse('message-list')
        invalid_data = {'text': 'Missing conservation field'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), 0)
    def test_mark_message_as_seen(self):
        message = Message.objects.create(text='Test Message', sender=self.user, conservation=self.conservation)
        url = reverse('message-mark-as-seen', args=[message.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(MessageSeenStatus.objects.filter(message=message, user=self.user, seen=True).exists())

    def test_get_unseen_messages(self):
        message = Message.objects.create(text='Test Message', sender=self.user, conservation=self.conservation)
        MessageSeenStatus.objects.create(message=message, user=self.user, seen=False)
        url = reverse('message-get-unseen-messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
