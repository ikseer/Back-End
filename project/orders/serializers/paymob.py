
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers


class PaymobOrderSerializer(serializers.ModelSerializer):
    paymob_order_id=serializers.CharField(read_only=True)
    paid=serializers.CharField(read_only=True)
    amount_cents=serializers.CharField(read_only=True)
    currency=serializers.CharField(read_only=True)
    class Meta:
        model = PaymobOrder
        fields = "__all__"
