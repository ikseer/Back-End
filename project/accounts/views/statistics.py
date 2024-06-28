
from accounts.models import Doctor, Patient
from accounts.serializers import StatisticsSerializer
from orders.models import Order
from pharmacy.models import Pharmacy
from products.models import Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class Statistics(GenericViewSet):
    serializer_class=StatisticsSerializer()
    def get(self, request, *args, **kwargs):
        data = {
            'total_patients': Patient.objects.count(),
            'total_doctors': Doctor.objects.count(),
            'total_pharmacies': Pharmacy.objects.count(),
            'total_products': Product.objects.count(),
            'total_orders': Order.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)
