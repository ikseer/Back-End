# -*- coding: utf-8 -*-
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *

User=get_user_model()

class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()


class VerifyMobileOtpSerializer(serializers.Serializer):
    otp = serializers.CharField()
    phone = serializers.CharField()


class UnlinkProviderSerializer(serializers.Serializer):
    provider = serializers.CharField()


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


# from dj_rest_auth.serializers import UserDetailsSerializer


class CustomRegistration(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(
        choices=['patient','doctor'],
        required=False
    )


class PatientSerializer(serializers.ModelSerializer):
    phone=serializers.SerializerMethodField()
    class Meta:
        model = Patient
        exclude = []
        extra_fields=['phone']


    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["email"] = instance.user.email
        representation["username"] = instance.user.username
        # if not instance.image:
        #     representation["image"] = "media/default/user.jpg"
        return representation
    def get_phone(self, obj):
        phones = PhoneModel.objects.filter(user=obj.user)
        return PhoneSerializer(phones,many=True).data

class DoctorSerializer(serializers.ModelSerializer):
    phone=serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        exclude = []
        extra_fields=['phone']

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["email"] = instance.user.email
        representation["username"] = instance.user.username

        return representation
    def get_phone(self, obj):
        phones = PhoneModel.objects.filter(user=obj.user)
        phones= PhoneSerializer(phones, many=True).data
        return phones


class loginSerializer(LoginSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def validate_email(self, value):
        user = self.context["request"].user
        if not user.emailaddress_set.filter(email=value, verified=True).exists():
            raise serializers.ValidationError(("E-mail is not verified."))
        return value


class OtpByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyEmailOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields ='__all__'
        exclude=['password']





class StatisticsSerializer(serializers.Serializer):
    total_patients=serializers.IntegerField()
    total_doctors=serializers.IntegerField()
    total_pharmacies=serializers.IntegerField()
    total_products=serializers.IntegerField()
    total_orders=serializers.IntegerField()



class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=PhoneModel
        # fields=['id','Mobile','isVerified']
        fields='__all__'
