
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
from rest_framework import viewsets

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
    pagination_class = ProductPagination
