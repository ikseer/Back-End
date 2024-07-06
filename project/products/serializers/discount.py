

from products.models import *
from rest_framework import serializers

from .image import *


class DiscountSerializer(serializers.ModelSerializer):
    before_price = serializers.SerializerMethodField()
    after_price=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model = Discount
        fields = "__all__"
    def get_image(self,obj):
        image= ProductImage.objects.filter(product=obj.product).order_by('priority').first()
        return ProductImageSerializer(image).data['image']
    def get_before_price(self,obj):
        return obj.product.price
    def get_after_price(self, obj):
        return obj.apply_discount(obj.product.price)
    #     return round(obj.product.price - (obj.percentage * obj.product.price / 100), 0)




class DiscountHomeSerializer(serializers.ModelSerializer):
    before_price = serializers.SerializerMethodField()
    after_price=serializers.SerializerMethodField()
    class Meta:
        model = Discount
        # fields = "__all__"
        exclude=['product']

    def get_before_price(self,obj):
        return obj.product.price
    def get_after_price(self, obj):
        return obj.apply_discount(obj.product.price)
