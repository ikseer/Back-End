
from products.models import *
from rest_framework import serializers


class ProductRatingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ProductRating
        fields = "__all__"
