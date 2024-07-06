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

        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.patient=Patient.objects.create(user=self.user)
        self.doctor=Doctor.objects.create(user=self.user2)

        self.conversation = Conversation.objects.create(patient=self.patient,doctor=self.doctor)

    def test_create_message(self):
        url = reverse('message-list')
        data = {'conversation': self.conversation.id, 'text': 'A test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'A test message')
        self.assertEqual(Message.objects.get().sender, self.user)
        url= reverse('conversation-list')
        response = self.client.get(url, format='json')

    def test_list_messages(self):
        url = reverse('message-list')
        data = {'conversation': self.conversation.id, 'text': 'A test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url= reverse('conversation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),1)
    def test_retrieve_message(self):
        message = Message.objects.create(conversation=self.conversation, text='A test message', sender=self.user)
        url = reverse('message-detail', args=[message.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'A test message')

    def test_update_message(self):
        message = Message.objects.create(conversation=self.conversation, text='A test message', sender=self.user)
        url = reverse('message-detail', args=[message.id])
        data = {'text': 'An updated test message'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.get().text, 'An updated test message')

    def test_partial_update_message(self):
        message = Message.objects.create(conversation=self.conversation, text='A test message', sender=self.user)
        url = reverse('message-detail', args=[message.id])
        data = {'text': 'A partially updated test message'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.get().text, 'A partially updated test message')

    def test_delete_message(self):
        message = Message.objects.create(conversation=self.conversation, text='A test message', sender=self.user)
        url = reverse('message-detail', args=[message.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)
