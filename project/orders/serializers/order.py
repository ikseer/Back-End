
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers

from .order_item import *


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True ,read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['customer', 'created_at', 'updated_at','products','status']  # Add other fields to this list as needed




    def create(self, validated_data):
        user = validated_data['user']
        cart_items = CartItem.objects.filter(cart__user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Cannot create order. Add at least one product to the cart.")

        order = Order.objects.create(**validated_data)

        # order = Order.objects.create(user=user)
        total_price = 0

        for cart_item in cart_items:
            order_item_data = {
                'order': order.id,
                'product': cart_item.product.id,
                'quantity': cart_item.quantity
            }
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()

            total_price += cart_item.get_total_price()
            cart_item.delete()

        order.total_price = total_price
        order.save()

        return order
