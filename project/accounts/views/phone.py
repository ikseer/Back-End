

from accounts.filters import *
from accounts.models import *
from accounts.pagination import *
from accounts.permissions import StaffPermission
from accounts.serializers import *
from accounts.utils import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from .views import *


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = PhoneModel.objects.all()
    serializer_class = PhoneModelSerializer
    pagination_class=CustomPagination
    permission_classes=[StaffPermission]
    filter_backends = [
            DjangoFilterBackend,
            rest_filters.SearchFilter,
            rest_filters.OrderingFilter,
        ]
    filterset_class = PhoneFilter
