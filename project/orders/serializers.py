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
    status=serializers.CharField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True ,read_only=True)
    class Meta:
        model = Order
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    class Meta:
        model =CartItem
        fields='__all__'
        extra_fields =['product_name']
        # fields=['id','product','product_name','quantity','cart']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model =Cart
        # fields='__all__'
        fields=['id','customer','items']
        # extra_fields =['items']
