

# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields ='__all__'
        exclude=['password']
