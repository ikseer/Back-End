# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class CouponFilter(filters.FilterSet):
    class Meta:
        model = Coupon
        fields = "__all__"
