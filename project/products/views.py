# -*- coding: utf-8 -*-
from decouple import config
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import *
from products.decorators import cache_production
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import *
from .models import *
from .pagination import *
from .permissions import *
from .serializers import *

use_cache=config('use_cache',0)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [SafePermission]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [SafePermission]
    pagination_class = ProductPagination
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]

    def get_top_selling_products(self):
        top_products = Product.objects.annotate(
            total_sales=Sum("orderitem__quantity")
        ).order_by("-total_sales")
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_production(60*5*use_cache))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_production(60*5*use_cache))  # Cache for 60 seconds
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    filterset_class = DiscountFilter
    permission_classes = [SafePermission]


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [SafePermission]
    filterset_class = ProductImageFilter


class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [SafePermission]
    filterset_class = ProductRatingFilter


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [SafePermission]
    filterset_class = WishlistFilter


class HomeView(GenericViewSet, mixins.ListModelMixin):
    queryset = Product.objects.all().order_by("id")
    serializer_class = HomeSerializer
    # permission_classes = [SafePermission]
    pagination_class = ProductPagination
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]

    def get_top_selling_products(self):
        top_products = Product.objects.annotate(
            total_sales=Sum("orderitem__quantity")
        ).order_by("-total_sales")
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_production(60*5))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [SafePermission]
    filterset_class = CouponFilter
