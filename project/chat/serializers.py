# myapp/serializers.py
from accounts.serializers import DoctorSerializer, PatientSerializer
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
        # fields = ['id', 'conversation', 'sender', 'text', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    patient_profile= serializers.SerializerMethodField()
    doctor_profile=serializers.SerializerMethodField()
    # users = UserSerializer(many=True, read_only=True)
    # doctor=DoctorSerializer()
    # patient=PatientSerializer()
    class Meta:
        model = Conversation
        # fields = ['id', 'name', 'description', 'users', 'messages']
        fields ='__all__'
        # extra_fields=['message']
    def get_message(self,obj):
        last_message = Message.objects.filter(conversation=obj).order_by('-created_at').first()
        if last_message is not None:
            return MessageSerializer(last_message).data
        else:
            return None
    def get_patient_profile(self,obj):
        return PatientSerializer(obj.patient).data
    def get_doctor_profile(self,obj):
        return DoctorSerializer(obj.doctor).data

class MessageSeenStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageSeenStatus
        fields = '__all__'

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=FCMToken
        fields='__all__'
