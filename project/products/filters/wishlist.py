# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class WishlistItemFilter(filters.FilterSet):
    class Meta:
        model = WishlistItem
        fields = "__all__"
