from .models import *
from rest_framework import serializers
from products.models import *
from products.serializers import *
class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model=Order
        fields='__all__'
