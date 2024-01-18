import email
import profile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from django.core import mail
import re

from accounts.models import EmailVerificationOTP, Profile
User = get_user_model()
class UserTest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
    def test_registration(self):
        url = reverse('rest_register')
        
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_not_created_profile(self):
        self.test_registration()

        profile = Profile.objects.get(user__email=self.data['email'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(profile.user.email, self.data['email'])
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().email, 'test@example.com')
   
    def test_login_unconfirmed_email(self):
        url = reverse('rest_login')
        response=self.client.post(url,{   'email': 'test@example.com',  'password': 'testpassword'})
        self.assertEqual(response.status_code,400)

    def test_email_confirmation(self):
        self.test_registration()

        
        st=mail.outbox[-1].body.find(":")+1
        otp=mail.outbox[-1].body[st:].strip()
        url=reverse('signup_verify', kwargs={'otp':otp})
        response=self.client.post(url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_login_confirmed_email(self):
        self.test_email_confirmation()
        url = reverse('rest_login')
        response=self.client.post(url,{   'email': 'test@example.com',  'password': 'testpassword'})
        # print(response.data)
        self.assertEqual(response.status_code,200)

    


        





class PasswordResetTests(APITestCase):
    def test_password_reset_request(self):
        user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')
        url = reverse('rest_password_reset')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        # print(mail.outbox[0].body)
        # self.assertEqual(mail.outbox[0].subject, 'Password reset on example.com')

    def test_password_reset_confirm(self):
        # Create a user object
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

      
        response = self.client.post(reverse('rest_password_reset'),  {'email': 'test@example.com'})
        # print(mail.outbox[0].body)
        st=mail.outbox[0].body.find('http')
        link = mail.outbox[0].body[st:]
        link=link[:link.find('\n')]
        pattern = r'http://testserver/accounts/rest-auth/password/reset/confirm/(?P<uid>[\w-]+)/(?P<token>[\w-]+)'

        match = re.search(pattern, link)


        uid = match.group('uid')
        token = match.group('token')
        # print(uid,token)
       
        data = {
            'uid': uid,
            'token': token,
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        }

        # Make the POST request to the password reset confirmation URL
        url = reverse('rest_password_reset_confirm')
        response = self.client.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password has been reset with the new password.')

    def test_password_change(self):
        user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=user)
        url = reverse('rest_password_change')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'New password has been saved.')

from django.test import TestCase

class AccessTokenTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    
        # Create a user with valid credentials
        user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')

        # Create an EmailAddress object for the user
        email_address = EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        url = reverse('rest_login')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = cls.client.post(url, data)
        cls.assertEqual(response.status_code, status.HTTP_200_OK)
        cls.access_token = response.data.get('access_token', None)
        # print(response.data,'*****')
        # print(cls.access_token)
