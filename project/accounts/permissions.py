# -*- coding: utf-8 -*-
# permissions.py
from rest_framework.permissions import BasePermission


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user



class IsAdminOrIsSelf(BasePermission):
    """
    Custom permission to only allow admins to create users.
    Users can get, update, and delete their own data.
    """
    def has_permission(self, request, view):

        if  request.method == 'DELETE':
            return True
            # return obj == request.user or request.user.is_staff

        return  request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #      return obj == request.user or request.user.is_staff


        if  request.method == 'DELETE':
            return obj == request.user or request.user.is_staff

        return request.user.is_staff



class StaffPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return  request.user.is_staff
