# -*- coding: utf-8 -*-
from decouple import config
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from orders.models import *
from orders.pagination import *
from orders.permissions import *
from orders.serializers import *
from orders.utils import check_paymob_order_status, create_paymob
from paymob.accept.callbacks import AcceptCallback
from rest_framework import filters as rest_filters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymobCallbackViewSet(APIView):
    def post(self, request, *args, **kwargs):
        """
        receive callback from paymob and update order status
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        callback_dict = request.data
        incoming_hmac =  config("INCOMING_HMAC", None)
        callback = AcceptCallback(
            incoming_hmac=incoming_hmac,
            callback_dict=callback_dict
        )
        if callback.is_valid and callback.obj.order.paid_amount_cents >= callback.obj.order.amount_cents:
            paymob=PaymobOrder.objects.get(paymob_order_id=callback.obj.order.id)
            paymob.paid=True
            paymob.save()
            return Response({"success":True})
        return Response({"success":False})


class PaymobOrderView(GenericAPIView):

    queryset = PaymobOrder.objects.all()
    serializer_class = PaymobOrderSerializer
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    # filter_backends = [
    #     PaymobOrderFilter
    # ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('order_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Order ID', required=True),
            openapi.Parameter('check_paid', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Check if order is paid', required=False),
        ]
    )


    def get(self, request, *args, **kwargs):
        orderId = request.query_params.get("order_id", None)
        get_object_or_404(Order, id=orderId)

        check_paid = request.query_params.get("check_paid", None)

        paymob=PaymobOrder.objects.filter(order__id=orderId).first()
        if paymob is not None:

            if check_paid and paymob.paid is False:
                if check_paymob_order_status(paymob.paymob_order_id):
                    paymob.paid=True
                    paymob.save()

        else:
            paymob=create_paymob(orderId)
            if paymob is None:
                return Response({"message": "Cannot create paymob order"}, status=status.HTTP_404_NOT_FOUND)
        return  Response(PaymobOrderSerializer(paymob).data)
