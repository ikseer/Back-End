# -*- coding: utf-8 -*-
# permissions.py
from rest_framework.permissions import BasePermission


class ProfilePermission(BasePermission):
    # def has_permission(self, request, view):
    #     if not request.user.is_authenticated :
    #         return False
    #     if request.user.is_staff or
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
