# -*- coding: utf-8 -*-

from django_filters.rest_framework import DjangoFilterBackend
from orders.models import *
from orders.pagination import *
from orders.permissions import *
from orders.serializers import *
from orders.utils import check_all_paymob
from rest_framework import filters as rest_filters
from rest_framework import viewsets


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        user = self.request.user
        return Order.objects.filter(user=user)
    def list(self, request, *args, **kwargs):

        check_all_paymob()
        return super().list(request, *args, **kwargs)
    # def create(self, request, *args, **kwargs):
    #     serializer=OrderSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     cart_items=CartItem.objects.filter(cart__user=serializer.data['user'])

    #     if len( cart_items)==0:
    #         return Response({"error": "Cannot create order. Add at least one product to the cart."},
    #                         status=status.HTTP_400_BAD_REQUEST)

    #     response= super().create(request, *args, **kwargs)
    #     order = Order.objects.get(id=response.data['id'])
    #     total_price = 0
    #     for cart_item in cart_items:
    #         order_item_serializer=OrderItemSerializer(data={'order':order.id,'product':cart_item.product.id,'quantity':cart_item.quantity})
    #         if not order_item_serializer.is_valid():
    #                 return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         OrderItem.objects.create(order=order,product=cart_item.product,quantity=cart_item.quantity)
    #         total_price+=cart_item.get_total_price()
    #         cart_item.delete()

    #     order.total_price=total_price
    #     order.save()

    #     return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemPermission]
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()

        return OrderItem.objects.filter(order__user=self.request.user)
