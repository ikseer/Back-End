from unittest.mock import patch

from chat.models import *
from chat.utils import *  # Import your functions to be tested
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User=get_user_model()

class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='test2', password='testpassword')
        self.fcm_token = FCMToken.objects.create(user=self.user2, token='fake_token')

        # self.profile = FCMToken.objects.create(user=self.user, token='fake_token')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.conversation = Conversation.objects.create(name='Test Conversation', description='A test conversation')
        self.conversation.users.add(self.user)
        self.conversation.users.add(self.user2)


    def test_send_notification_on_new_message(self):
        url = reverse('message-list')
        data = {'conversation': self.conversation.id, 'text': 'A test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MessageSeenStatus.objects.count(),1)
        # Ensure that notification sending is logged or check side effects

    def test_update_fcm_token(self):
        url = reverse('fcm-token-list')
        self.user2 = User.objects.create_user(username='test', password='testpassword')
        data = {'user':self.user2.id,'token': 'new_fake_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user2.fcm_token.token, 'new_fake_token')



class MessageUtilsTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.sender = User.objects.create(username='sender')
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.fcm_token_user1 = FCMToken.objects.create(user=self.user1, token='token_user1')
        self.fcm_token_user2 = FCMToken.objects.create(user=self.user2, token='token_user2')
        self.conversation = Conversation.objects.create(name='Test Conversation')
        self.conversation.users.add(self.sender, self.user1, self.user2)
        self.message = Message.objects.create(sender=self.sender, conversation=self.conversation, text='Hello')



    def test_unseen_message_message_seen_status_created(self):
        # Simulate calling unseen_message function
        unseen_message(self.message)

        # Assert that MessageSeenStatus objects are created
        message_seen_statuses = MessageSeenStatus.objects.filter(message=self.message)
        self.assertEqual(message_seen_statuses.count(), 2)  # Assuming there are two users in the conversation

        # Check if the created objects correspond to the expected users
        for user in [self.user1, self.user2]:
            self.assertTrue(message_seen_statuses.filter(user=user).exists())



    @patch('chat.utils.send_notification')
    @patch('chat.models.MessageSeenStatus.objects.create')
    def test_unseen_message_notification_sent(self, mock_message_seen_status_create, mock_send_notification):
        # Mock the return values or behavior of the mocked functions
        mock_message_seen_status_create.side_effect = lambda **kwargs: MessageSeenStatus(**kwargs)
        mock_send_notification.return_value = 'Notification sent'

        # Call the function you want to test
        unseen_message(self.message)


        mock_send_notification.assert_called_once()

    # @patch('chat.utils.send_notification')
    # def test_unseen_message_no_notification_sent_without_tokens(self, mock_send_notification):
    #     # Delete FCM tokens to simulate no tokens scenario
    #     self.user1.fcm_token.delete()
    #     self.user2.fcm_token.delete()

    #     # Call the function you want to test
    #     unseen_message(self.message)

    #     # Assertion
    #     mock_send_notification.assert_not_called()
