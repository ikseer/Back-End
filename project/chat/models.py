import uuid

from accounts.models import Doctor, Patient
from django.contrib.auth import get_user_model
from django.db import models

User=get_user_model()



class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Conversation(BaseModel):

    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_conv')
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_conv')
    class Meta:
        unique_together = ('doctor', 'patient')
    def __str__(self):
        return self.patient.user.username+" - "+self.doctor.user.username
class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.conversation.id} "


class MessageSeenStatus(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='seen_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seen_messages')
    seen = models.BooleanField(default=False)

class FCMToken(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="fcm_token")
    token=models.CharField(max_length=255,null=True,blank=True)
