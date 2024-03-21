# -*- coding: utf-8 -*-
from decouple import config
from paymob.accept.callbacks import AcceptCallback
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.utils import check_paymob_order_status

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
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        check_paid = request.query_params.get('check_paid', None)
        if check_paid   :
           paymob_order=PaymobOrder.objects.get(order__id=response.data["id"])

           if paymob_order.paid is False:
                if check_paymob_order_status(paymob_order.paymob_order_id):
                    paymob_order.paid=True
                    paymob_order.save()
                    response = super().retrieve(request, *args, **kwargs)

        return response
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
