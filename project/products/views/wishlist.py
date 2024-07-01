

# -*- coding: utf-8 -*-
from decouple import config
from orders.models import *
from products.filters import *
from products.models import *
from products.pagination import *
from products.permissions import *
from products.serializers import *
from rest_framework import viewsets

use_cache=config('use_cache',0)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [SafePermission]
    filterset_class = WishlistFilter
