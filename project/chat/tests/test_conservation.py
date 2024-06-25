# myapp/tests.py
from chat.models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class ConversationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_conversation(self):
        url = reverse('conversation-list')
        data = {'name': 'Test Conversation', 'description': 'A test conversation'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(Conversation.objects.get().name, 'Test Conversation')

    def test_list_conversations(self):
        conversation1 = Conversation.objects.create(name='Test Conversation 1', description='A test conversation')
        conversation2 = Conversation.objects.create(name='Test Conversation 2', description='Another test conversation')
        conversation1.users.add(self.user)
        conversation2.users.add(self.user)
        url = reverse('conversation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_conversation_detail(self):
        conversation = Conversation.objects.create(name='Test Conversation', description='A test conversation')
        conversation.users.add(self.user)
        url = reverse('conversation-detail', kwargs={'pk': conversation.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Conversation')
        self.assertEqual(response.data['description'], 'A test conversation')

    def test_update_conversation(self):
        conversation = Conversation.objects.create(name='Test Conversation', description='A test conversation')
        conversation.users.add(self.user)
        url = reverse('conversation-detail', kwargs={'pk': conversation.id})
        updated_data = {'name': 'Updated Conversation', 'description': 'An updated test conversation'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        conversation.refresh_from_db()
        self.assertEqual(conversation.name, 'Updated Conversation')
        self.assertEqual(conversation.description, 'An updated test conversation')

    def test_delete_conversation(self):
        conversation = Conversation.objects.create(name='Test Conversation', description='A test conversation')
        conversation.users.add(self.user)
        url = reverse('conversation-detail', kwargs={'pk': conversation.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_conversation_user_relationship(self):
        conversation = Conversation.objects.create(name='Test Conversation', description='A test conversation')
        conversation.users.add(self.user)
        url = reverse('conversation-detail', kwargs={'pk': conversation.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['username'], 'testuser')

    def test_conversation_invalid_data(self):
        url = reverse('conversation-list')
        invalid_data = {'description': 'Missing name field'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Conversation.objects.count(), 0)
