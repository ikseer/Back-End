from django.contrib.auth import get_user_model
from django.db import models

User=get_user_model()

class Conservation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='conservations')

    def __str__(self):
        return self.name

class Message(models.Model):
    conservation = models.ForeignKey(Conservation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.conservation.name} at {self.created_at}"
