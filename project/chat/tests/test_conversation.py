# myapp/tests.py
from chat.models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class ConversationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.patient=Patient.objects.create(user=self.user)
        self.doctor=Doctor.objects.create(user=self.user2)
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    def test_create_conversation(self):
        url = reverse('conversation-list')
        data = {'patient':self.patient.id,'doctor':self.doctor.id}
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)
        # self.assertEqual(Conversation.objects.get().name, 'Test Conversation')

    def test_list_conversations(self):
        url = reverse('conversation-list')
        data = {'patient':self.patient.id,'doctor':self.doctor.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('conversation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_conversation_detail(self):



        url = reverse('conversation-list')
        data = {'patient':self.patient.id,'doctor':self.doctor.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('conversation-detail', kwargs={'pk': response.data['id']})
        response = self.client.get(url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    # def test_update_conversation(self):
    #     url = reverse('conversation-detail', kwargs={'pk': self.conversation.id})
    #     new_doctor = Doctor.objects.create(user=self.user)
    #     data = {'doctor': new_doctor.id}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.conversation.refresh_from_db()
    #     self.assertEqual(self.conversation.doctor.id, new_doctor.id)

    # def test_delete_conversation(self):
    #     url = reverse('conversation-detail', kwargs={'pk': self.conversation.id})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Conversation.objects.count(), 0)

    # def test_create_conversation_unauthorized(self):
    #     self.client.credentials()  # Remove authentication
    #     url = reverse('conversation-list')
    #     data = {'patient': self.patient.id, 'doctor': self.doctor.id}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_update_conversation_unauthorized(self):
    #     self.client.credentials()  # Remove authentication
    #     url = reverse('conversation-detail', kwargs={'pk': self.conversation.id})
    #     new_doctor = Doctor.objects.create(user=self.user)
    #     data = {'doctor': new_doctor.id}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_delete_conversation_unauthorized(self):
    #     self.client.credentials()  # Remove authentication
    #     url = reverse('conversation-detail', kwargs={'pk': self.conversation.id})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_create_conversation_bad_data(self):
    #     url = reverse('conversation-list')
    #     data = {'patient': self.patient.id, 'doctor': 9999}  # Non-existent doctor
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_conversation_bad_data(self):
    #     url = reverse('conversation-detail', kwargs={'pk': self.conversation.id})
    #     data = {'doctor': 9999}  # Non-existent doctor
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
