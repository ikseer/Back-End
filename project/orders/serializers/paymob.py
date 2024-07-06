
from orders.models import *
from products.models import *
from products.serializers import *
from rest_framework import serializers


class PaymobOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymobOrder
        fields = "__all__"
        read_only_fields=['paymob_order_id','paid','amount_cents','currency']



class SavePaymobOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymobOrder
        fields = "__all__"
