

# -*- coding: utf-8 -*-
from decouple import config
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import *
from products.filters import *
from products.models import *
from products.pagination import *
from products.permissions import *
from products.serializers import *
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

use_cache=config('use_cache',0)


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

    # @method_decorator(cache_production(60*5*use_cache))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_production(60*5*use_cache))  # Cache for 60 seconds
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)




class HomeView(GenericViewSet, mixins.ListModelMixin):
    queryset = Product.objects.all().order_by("id")
    serializer_class = HomeSerializer
    # permission_classes = [SafePermission]
    pagination_class = ProductPagination
    filterset_class = HomeFilter
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

    # @method_decorator(cache_production(60*5))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
