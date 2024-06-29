# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()

class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
