from rest_framework import viewsets

from .models import *
from .serializers import *


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
