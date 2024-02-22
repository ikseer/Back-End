# permissions.py


from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


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

        return request.user.is_authenticated and obj.customer == request.user


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
        return request.user.is_authenticated and obj.order.customer == request.user
