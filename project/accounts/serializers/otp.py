# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()



class VerifyMobileOtpSerializer(serializers.Serializer):
    otp = serializers.CharField()
    phone = serializers.CharField()



class OtpByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyEmailOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
