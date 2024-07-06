
from chat.models import MessageSeenStatus
from firebase_admin import messaging

from .firebase_config import *


def send_notification(tokens,text):
        if tokens:

            message = messaging.MulticastMessage(
                tokens=tokens,
                notification=messaging.Notification(
                    title="New Message",
                    body=text,
                ),
            )
            response = messaging.send_multicast(message)
            return response


def unseen_message(message):
    tokens=[]
    for user in [message.conversation.patient.user,message.conversation.doctor.user]:
        if user==message.sender:
            continue
        MessageSeenStatus.objects.create(message=message, user=user)
        try:
             tokens.append(user.fcm_token.token)

        except Exception:
             pass
    send_notification(tokens,message.text)
