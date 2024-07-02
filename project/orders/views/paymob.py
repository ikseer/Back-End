# -*- coding: utf-8 -*-
# from urllib import request
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from orders.filters import *
from orders.models import *
from orders.pagination import *
from orders.permissions import *
from orders.serializers import *
from orders.utils import check_paymob_order_status, create_paymob
from paymob.accept.callbacks import AcceptCallback
from rest_framework import filters as rest_filters
from rest_framework import status, viewsets
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
        callback = AcceptCallback(
            incoming_hmac=request.query_params.get('hmac'),
            callback_dict=callback_dict
        )
        print(    callback.is_valid , callback.obj.order.paid_amount_cents , callback.obj.order.amount_cents)
        if  int(callback.obj.order.paid_amount_cents) >= int(callback.obj.order.amount_cents):
            paymob=PaymobOrder.objects.get(paymob_order_id=callback.obj.order.id)
            paymob.paid=True
            paymob.save()
            paymob.order.remove_items()

            return Response({"success":True})
        return Response({"success":False})











class PaymobOrderViewSet(   viewsets.ModelViewSet):


    queryset = PaymobOrder.objects.all()
    serializer_class = PaymobOrderSerializer
    pagination_class=CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = PaymobFilter
    def get_queryset(self):
        if not self.request.user.is_staff:
            return  PaymobOrder.objects.filter(order__user=self.request.user)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = PaymobOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.get(id=serializer.data['order'])

        paymob_order_id=create_paymob(order)
        if paymob_order_id is None:
                return Response({"message": "Cannot create paymob order"}, status=status.HTTP_404_NOT_FOUND)
        data={
            'order':order.id,
            'paymob_order_id':paymob_order_id,
            'amount_cents':order.total_price*100
        }

        serializer = SavePaymobOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


        # return super().create( request, *args, **kwargs)



    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'check_paid',
                openapi.IN_QUERY,
                description="Check if the order is paid it will send request to paymob",
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        # paymob=super().retrieve(request, *args, **kwargs)
        super().retrieve(request, *args, **kwargs)

        paymob=self.get_object()

        check_paid = request.query_params.get("check_paid", None)
        if check_paid  and not paymob.paid and  check_paymob_order_status(paymob.paymob_order_id):
                paymob.paid=True
                paymob.save()
                paymob.order.remove_items()



        return super().retrieve(request, *args, **kwargs)








    # filter_backends = [
    #     PaymobOrderFilter
    # ]

#     # @swagger_auto_schema(
#     #     manual_parameters=[
#     #         openapi.Parameter('order_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Order ID', required=True),
#     #         openapi.Parameter('check_paid', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Check if order is paid', required=False),
#     #     ]
#     # )


#     def create(self, request, *args, **kwargs):
#         serializer = CreatePaymobOrderSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         order = serializer.validated_data['id']

#         try:
#             paymob=PaymobOrder.objects.get(order=order)

#         except PaymobOrder.DoesNotExist:

#             paymob=create_paymob(order.id)
#             if paymob is None:
#                 return Response({"message": "Cannot create paymob order"}, status=status.HTTP_404_NOT_FOUND)

#         return  Response(PaymobOrderSerializer(paymob).data)
