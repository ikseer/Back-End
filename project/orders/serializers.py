# -*- coding: utf-8 -*-
from products.models import *
from products.serializers import *
from rest_framework import serializers

from .models import *

# class PaymobOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymobOrder
#         fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True ,read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['customer', 'created_at', 'updated_at','products','status']  # Add other fields to this list as needed


class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    product_final_price=serializers.CharField(source='product.get_final_price',read_only=True)
    product_image=serializers.SerializerMethodField()

    class Meta:
        model =CartItem
        fields='__all__'
        extra_fields =['product_name','product_final_price']
        # fields=['id','product','product_name','quantity','cart']
    def get_product_image(self,obj):
        first_image = ProductImage.objects.order_by('priority').first()
        if first_image:
            return ProductImageSerializer(first_image).data
        else:
            return None


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(source='cart__items', many=True, read_only=True)
    total_price=serializers.CharField(source='get_total_price',read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model =Cart
        fields='__all__'
        # fields=['id','user','items']
        extra_fields =['items']


# class CreatePaymobOrderSerializer(serializers.Serializer):
#     order_id = serializers.CharField()
#     def validate_order_id(self, value):
#         try:
#             order = Order.objects.get(id=value)
#         except Order.DoesNotExist:
#             raise serializers.ValidationError("Order does not exist.")
#         return order

# class CreatePaymobOrderSerializer(serializers.Serializer):
#     order_id = serializers.CharField()
#     def validate_order_id(self, value):
#         try:
#             order = Order.objects.get(id=value)
#         except Order.DoesNotExist:
#             raise serializers.ValidationError("Order does not exist.")
#         return order

class PaymobOrderSerializer(serializers.ModelSerializer):
    paymob_order_id=serializers.CharField(read_only=True)
    paid=serializers.CharField(read_only=True)
    amount_cents=serializers.CharField(read_only=True)
    currency=serializers.CharField(read_only=True)
    class Meta:
        model = PaymobOrder
        fields = "__all__"
