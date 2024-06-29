
# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()


class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()




class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=PhoneModel
        fields=['id','Mobile','isVerified']
        fields='__all__'
