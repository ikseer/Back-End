
# -*- coding: utf-8 -*-

from accounts.filters import *
from accounts.models import *
from accounts.permissions import ProfilePermission
from accounts.serializers import *
from accounts.utils import *
from rest_framework import viewsets

from .views import *

# -*- coding: utf-8 -*-





class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [ProfilePermission]
    filterset_class = DoctorFilter
