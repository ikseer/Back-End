# -*- coding: utf-8 -*-
from products.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


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


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    # final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    final_price=serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"
        extra_fields=['final_price','images','review','wishlist','discount']

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(images, many=True).data

    def get_review(self, obj):
        review = ProductRating.objects.filter(product=obj)
        return ProductRatingSerializer(review, many=True).data

    def get_wishlist(self, obj):
        # wishlist = Wishlist.objects.filter(product=obj)
        return WishlistSerializer(obj.wishlists, many=True).data

    def get_discount(self, obj):
        discount = Discount.objects.filter(product=obj)
        return DiscountSerializer(discount, many=True).data

    def get_final_price(self,obj):
        return obj.get_final_price()
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['final_price'] = instance.get_final_price()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductRatingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ProductRating
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"


class HomeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["generic_name", "name", "price", "image", "discount", "review"]

    def get_image(self, obj):
        image = ProductImage.objects.filter(product=obj).order_by("-priority")[0:1]
        return ProductImageSerializer(image, many=True).data

    def get_discount(self, obj):
        discount = Discount.objects.filter(product=obj).first()
        return DiscountSerializer(discount).data

    def get_review(self, obj):
        review = ProductRating.objects.filter(product=obj)
        total_sum = sum([review.rating for review in review])
        return round(total_sum / ((len(review))))
class CouponSerializer(serializers.ModelSerializer):
    code=serializers.CharField(read_only=True)
    class Meta:
        model = Coupon
        fields = "__all__"
