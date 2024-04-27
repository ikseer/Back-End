# -*- coding: utf-8 -*-
from products.models import *
from products.serializers import *
from rest_framework import serializers

from .models import *


class PaymobOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymobOrder
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True ,read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
