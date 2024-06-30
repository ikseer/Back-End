# -*- coding: utf-8 -*-

from accounts.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()


class EmployeeTest(APITestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(username='adminuser', password='adminpassword', email='adminuser@example.com', user_type='doctor', is_staff=True)

        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)

        # URLs
        self.user_list_url = reverse('customuser-list')
        self.user_detail_url = lambda pk: reverse('customuser-detail', kwargs={'pk': pk})

    def test_admin_can_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'user_type': 'employee'
        }
        response = self.client.post(self.user_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(),1)
