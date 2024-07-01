# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class WishlistFilter(filters.FilterSet):
    class Meta:
        model = Wishlist
        fields = "__all__"
