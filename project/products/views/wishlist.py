

# -*- coding: utf-8 -*-
from decouple import config
from orders.models import *
from products.filters import *
from products.models import *
from products.pagination import *
from products.permissions import *
from products.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

use_cache=config('use_cache',0)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = WishlistFilter
    pagination_class = ProductPagination
    def list(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            self.queryset= Wishlist.objects.filter(user=self.request.user)
        return super().list(request, *args, **kwargs)


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated, WishlistItemPermission]
    pagination_class = ProductPagination

    def get_queryset(self):
        if not self.request.user.is_staff:
            return WishlistItem.objects.filter(wishlist__user=self.request.user)
        return super().get_queryset()
