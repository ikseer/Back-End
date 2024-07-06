

# -*- coding: utf-8 -*-
import base64

from accounts.filters import *
from accounts.models import *
from accounts.pagination import *
from accounts.permissions import *
from accounts.permissions import StaffPermission
from accounts.serializers import *
from accounts.utils import *
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from orders.pagination import CustomPagination
# views.py
from rest_framework import filters as rest_filters
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .otp import generateKey

EXPIRY_TIME = getattr(settings, 'EXPIRY_TIME', 120)



class PhoneViewSet(viewsets.ModelViewSet):
    queryset = PhoneModel.objects.all()
    serializer_class = PhoneModelSerializer
    pagination_class=CustomPagination
    permission_classes=[StaffPermission]
    filter_backends = [
            DjangoFilterBackend,
            rest_filters.SearchFilter,
            rest_filters.OrderingFilter,
        ]
    filterset_class = PhoneFilter







class PhoneRegister(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhoneRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = PhoneRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        try:
            Mobile = PhoneModel.objects.get(
                Mobile=phone
            )  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            PhoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = PhoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.user = request.user
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model for OTP is created
        # send_otp_via_email(request, OTP.now())
        response_data = {
            "message": "OTP  sent to the mobile number ",
            "OTP": OTP.now(),
        }

        return Response(response_data, status=status.HTTP_200_OK)
