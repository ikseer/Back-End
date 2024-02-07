from .models import *
from rest_framework import serializers
from products.models import *
from products.serializers import *
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem  
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'
