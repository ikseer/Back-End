# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# user serializer

User = get_user_model()


class UserTest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "test",
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "gender": "male",
        }

        self.url  = reverse("rest_register")
    def test_registration(self):

        response = self.client.post(self.url, self.data)
        User.objects.get(email=self.data["email"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data["username"]="ali"
        response== self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url=reverse("otp-by-email")

        response== self.client.post(url,{"email":self.data["email"]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
