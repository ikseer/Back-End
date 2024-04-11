# -*- coding: utf-8 -*-
from decouple import config
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from orders.filters import PaymobOrderFilter
from orders.utils import check_paymob_order_status, create_paymob
from paymob.accept.callbacks import AcceptCallback
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

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
    # def retrieve(self, request, *args, **kwargs):
        # response = super().retrieve(request, *args, **kwargs)
        # check_paid = request.query_params.get('check_paid', None)
        # if check_paid   :
        #    paymob_order=PaymobOrder.objects.get(order__id=response.data["id"])

        #    if paymob_order.paid is False:
        #         if check_paymob_order_status(paymob_order.paymob_order_id):
        #             paymob_order.paid=True
        #             paymob_order.save()
        #             response = super().retrieve(request, *args, **kwargs)

        # return response
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()

        return OrderItem.objects.filter(order__customer=self.request.user)




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
    filter_backends = [
        PaymobOrderFilter
    ]

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
                return Response({"message": "Cannot create paymob order"}, status=404)
        return Response(PaymobOrderSerializer(paymob).data)
