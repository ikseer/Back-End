# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from django.core import mail
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

    def test_registration(self):
        url = reverse("rest_register")

        response = self.client.post(url, self.data)
        User.objects.get(email=self.data["email"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_created_profile(self):
        self.test_registration()
        profile = Patient.objects.first()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(profile.user.email, self.data["email"])
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_login_unconfirmed_email(self):
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 400)

    def test_email_confirmation(self):
        self.test_registration()
        st = mail.outbox[-1].body.find(":") + 1
        otp = mail.outbox[-1].body[st:].strip()
        url = reverse("verify-email-otp")
        response = self.client.post(url, {"otp": otp})

        # self.assertIn("profile", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        url = reverse("token_verify")
        response = self.client.post(url, {"token": access})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_confirmed_email(self):
        self.test_email_confirmation()
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        # login with username
        url = reverse("rest_login")
        response = self.client.post(
            url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        # print(response.data)

    def test_otp_by_email(self):
        self.test_login_confirmed_email()
        url = reverse("otp-by-email")
        response = self.client.post(url, {"email": "test@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_data(self):
        self.test_otp_by_email()
        # user and token
        User.objects.get(email=self.data["email"])
        # access token
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "testpassword"}
        )
        # print(response.data)
        access_token = response.data["access"]
        url = reverse("rest_user_details")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_email(self):
        self.test_user_data()
        url = reverse("check-email")
        response = self.client.post(url, {"email": "test@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email_exists'],True)
        # self.assertEqual(response.data['email_exists'],False)

        response = self.client.post(url, {"email": "test2@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email_exists'],False)



    def test_username(self):
        self.test_user_data()
        url = reverse("check-username")
        response = self.client.post(url, {"username": "testuser"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, {"username": "test2user"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username_exists'],False)



# # rest password otp


class PasswordResetTests(APITestCase):
    def setUp(self):
        url = reverse("rest_register")
        self.data = {
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "test",
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "gender": "male",
        }
        self.client.post(url, self.data)
        st = mail.outbox[-1].body.find(":") + 1
        otp = mail.outbox[-1].body[st:].strip()
        url = reverse("verify-email-otp")
        response = self.client.post(url, {"otp": otp})
        self.access = response.data["access"]
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.user = User.objects.get(email="test@example.com")

    def test_otp_by_email(self):
        url = reverse("otp-by-email")
        response = self.client.post(url, {"email": "test@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reseve_otp(self):
        url = reverse("otp-by-email")
        response = self.client.post(url, {"email": "test@example.com"})
        st = mail.outbox[-1].body.find(":") + 1
        otp = mail.outbox[-1].body[st:].strip()
        url = reverse("verify-email-otp")
        response = self.client.post(url, {"otp": otp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        url = reverse("rest_password_change")
        response = self.client.post(
            url,
            {
                "old_password": "testpassword",
                "new_password1": "testpassword1",
                "new_password2": "testpassword1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)





class CheckPasswordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.client.force_authenticate(user=self.user)

    def test_check_valid_password(self):
        url = reverse(
            "check-password"
        )  # Assuming you've named your URL pattern 'check-password'
        data = {"password": "test_password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['detail'], 'Password is valid')

    def test_check_invalid_password(self):
        url = reverse(
            "check-password"
        )  # Assuming you've named your URL pattern 'check-password'
        data = {"password": "wrong_password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['detail'], 'Password is invalid')
