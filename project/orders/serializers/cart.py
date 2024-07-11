
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers

from .cart_item import *


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(source='cart__items', many=True, read_only=True)
    total_price=serializers.CharField(source='get_total_price',read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model =Cart
        fields='__all__'
        # fields=['id','user','items']
        extra_fields =['items']
