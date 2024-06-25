# -*- coding: utf-8 -*-
from rest_framework import permissions

# permissions.py


class OrderPermission(permissions.BasePermission):
    """
    Custom permission to allow only administrators to list orders,
    while authenticated users can create, edit, and delete their own orders.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return request.user.is_authenticated and obj.user == request.user


class OrderItemPermission(permissions.BasePermission):
    """
    Custom permission to allow only administrators to list orders,
    while authenticated users can create, edit, and delete their own orders.
    """

    # def has_permission(self, request, view):

    #     return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user.is_authenticated and obj.order.user == request.user


class CartPermission(permissions.BasePermission):
    """
    Custom permission to allow only administrators to list orders,
    while authenticated users can create, edit, and delete their own orders.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return request.user.is_authenticated and obj.user == request.user


class CartItemPermission(permissions.BasePermission):
    """
    Custom permission to allow only administrators to list orders,
    while authenticated users can create, edit, and delete their own orders.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        # return request.user.is_authenticated and obj.user == request.user
        return request.user.is_authenticated and obj.cart.user == request.user
