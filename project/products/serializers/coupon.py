

from products.models import *
from rest_framework import serializers


class CouponSerializer(serializers.ModelSerializer):
    code=serializers.CharField(read_only=True)
    class Meta:
        model = Coupon
        fields = "__all__"
