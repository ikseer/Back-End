from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .permissions import *
from .serializers import *


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        user = self.request.user
        return Order.objects.filter(customer=user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()

        return OrderItem.objects.filter(order__customer=self.request.user)
