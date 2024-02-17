from rest_framework import serializers

from products.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        discount = Discount.objects.filter(product=instance).first()
        if discount:
            data = DiscountSerializer(discount).data
            data["old_price"] = instance.price
            data["current_price"] = int(
                instance.price - (discount.percentage * instance.price / 100)
            )
            representation["discount"] = data
        else:
            representation["discount"] = None
        images = ProductImage.objects.filter(product=instance)
        representation["images"] = ProductImageSerializer(images, many=True).data
        review = ProductRating.objects.filter(product=instance)
        representation["review"] = ProductRatingSerializer(review, many=True).data
        wishlist = Wishlist.objects.filter(product=instance)
        representation["wishlist"] = WishlistSerializer(wishlist, many=True).data
        return representation


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
