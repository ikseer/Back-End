# myapp/tests.py
from chat.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class ConservationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_conservation(self):
        url = reverse('conservation-list')
        data = {'name': 'Test Conservation', 'description': 'A test conservation'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conservation.objects.count(), 1)
        self.assertEqual(Conservation.objects.get().name, 'Test Conservation')

    def test_list_conservations(self):
        conservation1 = Conservation.objects.create(name='Test Conservation 1', description='A test conservation')
        conservation2 = Conservation.objects.create(name='Test Conservation 2', description='Another test conservation')
        conservation1.users.add(self.user)
        conservation2.users.add(self.user)
        url = reverse('conservation-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_conservation_detail(self):
        conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        conservation.users.add(self.user)
        url = reverse('conservation-detail', kwargs={'pk': conservation.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Conservation')
        self.assertEqual(response.data['description'], 'A test conservation')

    def test_update_conservation(self):
        conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        conservation.users.add(self.user)
        url = reverse('conservation-detail', kwargs={'pk': conservation.id})
        updated_data = {'name': 'Updated Conservation', 'description': 'An updated test conservation'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        conservation.refresh_from_db()
        self.assertEqual(conservation.name, 'Updated Conservation')
        self.assertEqual(conservation.description, 'An updated test conservation')

    def test_delete_conservation(self):
        conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        conservation.users.add(self.user)
        url = reverse('conservation-detail', kwargs={'pk': conservation.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Conservation.objects.count(), 0)

    def test_conservation_user_relationship(self):
        conservation = Conservation.objects.create(name='Test Conservation', description='A test conservation')
        conservation.users.add(self.user)
        url = reverse('conservation-detail', kwargs={'pk': conservation.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['username'], 'testuser')

    def test_conservation_invalid_data(self):
        url = reverse('conservation-list')
        invalid_data = {'description': 'Missing name field'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Conservation.objects.count(), 0)
