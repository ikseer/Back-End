# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from pharmacy.filters import PharmacyFilter
from pharmacy.pagination import CustomPagination
from products.permissions import SafePermission
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from .models import *
from .serializers import *


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [SafePermission]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = PharmacyFilter
    pagination_class = CustomPagination
