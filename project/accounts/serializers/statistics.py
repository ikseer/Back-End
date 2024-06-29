# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()









class StatisticsSerializer(serializers.Serializer):
    total_patients=serializers.IntegerField()
    total_doctors=serializers.IntegerField()
    total_pharmacies=serializers.IntegerField()
    total_products=serializers.IntegerField()
    total_orders=serializers.IntegerField()
