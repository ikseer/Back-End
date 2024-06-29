# -*- coding: utf-8 -*-

from accounts.models import *
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()
# testcase

# testcase


class DoctorTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "test",
            "last_name": "test",
            "gender": "male",
            "user_type":"doctor"
        }
        self.patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "bio": "This is a test bio.",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
        }

        # Create a user and obtain a token for authentication
        url = reverse("rest_register")
        response=self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code,201)
        # confirm email


        st = mail.outbox[-1].body.find(":") + 1
        otp = mail.outbox[-1].body[st:].strip()
        url = reverse("verify-email-otp")
        self.client.post(url, {"otp": otp})
        # print(response)

        self.user = User.objects.get(email=self.user_data["email"])
        # self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    def test_doctor_created(self):
        doctor=Doctor.objects.all()
        patient=Patient.objects.all()


        self.assertEqual(len(doctor),1)
        self.assertEqual(len(patient),0)
    def test_get_doctor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.post(
            reverse("phone-register"), {"phone": "01015321456"}
        )
        # print('*'*50)
        # print(PhoneModel.objects.first().user,self.user)
        # print(response.data )
        response=self.client.get(f'/accounts/doctor/?user={self.user.id}')
        self.assertEqual(response.status_code,200)
        # print(response.data)
