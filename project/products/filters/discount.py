

# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class DiscountFilter(filters.FilterSet):
    class Meta:
        model = Discount
        fields = "__all__"
