# -*- coding: utf-8 -*-
from accounts.models import *
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()




class UnlinkProviderSerializer(serializers.Serializer):
    provider = serializers.CharField()



# from dj_rest_auth.serializers import UserDetailsSerializer


class CustomRegistration(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(
        choices=['patient','doctor'],
        required=False
    )



class loginSerializer(LoginSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def validate_email(self, value):
        user = self.context["request"].user
        if not user.emailaddress_set.filter(email=value, verified=True).exists():
            raise serializers.ValidationError(("E-mail is not verified."))
        return value
