# test patient views
from accounts.models import *
# from accounts.tests.test_setup import HomeTestSetup
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

User= get_user_model()
class TestSetup(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "test",
            "last_name": "test",
            "gender": "male",
        }


    def get_token(self, username, password):
        token = self.client.post(
            '/accounts/login/', {'username': username, 'password': password}, format='json')
        # if 'access' not in token.data:
        # print('no access',token.data,username,password)
        self.assertEqual(token.status_code, 200)
        return token.data['access']

    def create_staff(self, username='stafftest', password='test123'):
        user = User.objects.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        token = self.get_token(username, password)
        return user, token

    def create_user(self):
        user = User.objects.create_user(username='test', password='test123')
        return user

    def create_patient(self):

        url = reverse("rest_register")
        self.client.post(url, self.user_data, format="json")
        user=CustomUser.objects.get(username=self.user_data['username'])
        EmailAddress.objects.create(user=user,verified=True)

        token = self.get_token(self.user_data['username'], self.user_data['password1'])
        patient=Patient.objects.get(user=user)

        return  patient,token
    def create_doctor(self):

        url = reverse("rest_register")
        self.user_data['user_type']='doctor'
        self.client.post(url, self.user_data, format="json")
        user=CustomUser.objects.get(username=self.user_data['username'])
        EmailAddress.objects.create(user=user,verified=True)

        token = self.get_token(self.user_data['username'], self.user_data['password1'])
        doctor=Doctor.objects.get(user=user)

        return  doctor,token
