
from rest_framework import serializers

from products.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Discount
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        discount=Discount.objects.filter(product=instance).first()
        if discount:
            data=DiscountSerializer(discount).data
            data['old_price']=instance.price
            data['current_price'] = int(instance.price-(discount.percentage * instance.price/100))
            representation['discount']=data
        
        return representation
     

