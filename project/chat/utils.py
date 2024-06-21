
from chat.models import MessageSeenStatus

# from .firebase_config import messaging


def send_notification(tokens,text):
        if tokens:
             pass
            # message = messaging.MulticastMessage(
            #     tokens=tokens,
            #     notification=messaging.Notification(
            #         title="New Message",
            #         body=text,
            #     ),
            # )
            # response = messaging.send_multicast(message)
            # return response


def unseen_message(message):
    tokens=[]
    for user in message.conservation.users.all():
        if user==message.sender:
            continue

        MessageSeenStatus.objects.create(message=message, user=user)
        if user.fcm_token.token:
             tokens.append(user.fcm_token.token)
    send_notification(tokens,message.text)
