# -*- coding: utf-8 -*-
from django.urls import include, path
from orders.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("order-item", OrderItemViewSet)
router.register('cart',CartViewSet)
router.register('cart-item',CartItemViewSet)
router.register('paymob',PaymobOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("paymob-callback/", PaymobCallbackViewSet.as_view(), name="paymob-callback"),
    # path("paymob-order/", PaymobOrderView.as_view(), name="paymob-order"),
    # path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    # path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
]
