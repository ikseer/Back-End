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
        fields='__all__'
        # fields = ['id', 'conservation', 'sender', 'text', 'created_at']

class ConservationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conservation
        fields = ['id', 'name', 'description', 'users', 'messages']


class MessageSeenStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageSeenStatus
        fields = '__all__'

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=FCMToken
        fields='__all__'
