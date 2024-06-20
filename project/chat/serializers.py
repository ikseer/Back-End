# myapp/serializers.py
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conservation', 'sender', 'text', 'created_at']

class ConservationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conservation
        fields = ['id', 'name', 'description', 'users', 'messages']
