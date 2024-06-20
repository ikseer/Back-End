
# -*- coding: utf-8 -*-

from django_filters.rest_framework import DjangoFilterBackend
from orders.models import *
from orders.pagination import *
from orders.permissions import *
from orders.serializers import *
from rest_framework import filters as rest_filters
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CartViewSet(
                # mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                # mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet
                ):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes = [CartPermission]
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    # filterset_class =
    def list(self,request,*args,**kwargs):

        if not self.request.user.is_staff:
            cart= Cart.objects.filter(user=self.request.user).first()

            return Response(CartSerializer(cart).data,status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer
    permission_classes = [CartItemPermission]
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
