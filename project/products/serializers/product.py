
from products.models import *
from rest_framework import serializers

from .discount import *
from .image import *
from .rating import *
from .wishlist import *


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    # wishlist = serializers.SerializerMethodField()
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

    # def get_wishlist(self, obj):
    #     # wishlist = Wishlist.objects.filter(product=obj)
    #     return WishlistSerializer(obj.wishlists, many=True).data

    def get_discount(self, obj):
        discount = Discount.objects.filter(product=obj)
        return DiscountSerializer(discount, many=True).data

    def get_final_price(self,obj):
        return obj.get_final_price()
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['final_price'] = instance.get_final_price()




class HomeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id","generic_name", "name", "price", "image", "discount", "review","stock","number_of_sales"]

    def get_image(self, obj):
        image = ProductImage.objects.filter(product=obj).order_by("-priority").first()
        if not image:
            return None
        return ProductImageSerializer(image).data['image']

    def get_discount(self, obj):
        discount = Discount.objects.filter(product=obj,active=True).first()
        if not discount:
            return None
        return DiscountHomeSerializer(discount).data

    def get_review(self, obj):
        review = ProductRating.objects.filter(product=obj)
        total_sum = sum([review.rating for review in review])
        return round(total_sum / ((len(review))))
