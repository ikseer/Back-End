


from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers


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
        first_image = ProductImage.objects.filter(product=obj.product).order_by('priority').first()
        if first_image:
            return ProductImageSerializer(first_image).data['image']
        else:
            return None
    def validate(self, attrs):
        response= super().validate(attrs)
        product = attrs['product']
        quantity = attrs['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError({
                'quantity': f"Only {product.stock} items in stock, but {quantity} requested."
            })
        return response
