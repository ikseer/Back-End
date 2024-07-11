
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers


class ProductOfOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    product_details = ProductOfOrderItemSerializer(source="product",read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"
        extra_fields=['product_details']

    def validate(self, attrs):
        response= super().validate(attrs)

        product = attrs['product']
        quantity = attrs['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError({
                'quantity': f"Only {product.stock} items in stock, but {quantity} requested."
            })
        return response
