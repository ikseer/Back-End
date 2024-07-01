# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class ProductImageFilter(filters.FilterSet):
    class Meta:
        model = ProductImage
        exclude = ["image"]
