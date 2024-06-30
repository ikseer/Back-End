
# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .phone import PhoneSerializer

User=get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    phone=serializers.SerializerMethodField()
    class Meta:
        model = Employee
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




class RestoreEmployeeSerializer(serializers.Serializer):
    id = serializers.CharField()
    def validate_id(self, value):
        try:
            employee=Employee.deleted_objects.get(id=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee does not exist.")
        return employee
