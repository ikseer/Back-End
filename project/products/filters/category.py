# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "name": ["exact", "icontains", "istartswith"],
        }
