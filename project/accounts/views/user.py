# -*- coding: utf-8 -*-

from accounts.filters import *
from accounts.models import *
from accounts.models import CustomUser
from accounts.permissions import *
from accounts.serializers import *
from accounts.serializers import CustomUserSerializer
from accounts.utils import *
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from orders.pagination import CustomPagination
# views.py
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

EXPIRY_TIME = getattr(settings, 'EXPIRY_TIME', 120)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class=CustomPagination
    permission_classes=[IsAuthenticated,IsAdminOrIsSelf]
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        user_type=response.data['user_type']
        user = User.objects.get(id=response.data['id'])
        POSITIONS[user_type].objects.create(user=user)

        return response
    



class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class=CustomPagination

class PermissionViewSet(
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet
    ):
    permission_classes = [IsAdminUser]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class=CustomPagination
