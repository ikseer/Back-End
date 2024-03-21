from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile

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
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["is_completed"]

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["email"] = instance.user.email
        representation["username"] = instance.user.username
        if not instance.image:
            representation["image"] = "media/default/user.jpg"
        return representation


class CustomUserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer()  # Replace with your actual profile serializer


class loginSerializer(LoginSerializer):
    class Meta:
        model = Profile
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
