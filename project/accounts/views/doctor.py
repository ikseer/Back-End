
from .views import *


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [ProfilePermission]
    filterset_class = DoctorFilter
