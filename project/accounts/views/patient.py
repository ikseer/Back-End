
# -*- coding: utf-8 -*-

from accounts.filters import *
from accounts.models import *
from accounts.pagination import *
from accounts.permissions import ProfilePermission
from accounts.serializers import *
from accounts.utils import *
from rest_framework import viewsets

from .views import *

# -*- coding: utf-8 -*-




class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [ProfilePermission]
    filterset_class = PatientFilter
    pagination_class=CustomPagination
