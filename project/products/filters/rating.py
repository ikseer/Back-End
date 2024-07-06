
# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class ProductRatingFilter(filters.FilterSet):
    class Meta:
        model = ProductRating
        fields = "__all__"
