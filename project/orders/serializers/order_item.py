
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"

    def validate(self, attrs):
        response= super().validate(attrs)

        product = attrs['product']
        quantity = attrs['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError({
                'quantity': f"Only {product.stock} items in stock, but {quantity} requested."
            })
        return response
