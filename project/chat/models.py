import uuid

from django.contrib.auth import get_user_model
from django.db import models

User=get_user_model()



class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Conservation(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='conservations')

    def __str__(self):
        return self.name
class Message(BaseModel):
    conservation = models.ForeignKey(Conservation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.conservation.name} "


class MessageSeenStatus(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='seen_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seen_messages')
    seen = models.BooleanField(default=False)

class FCMToken(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="fcm_token")
    token=models.CharField(max_length=255,null=True,blank=True)
