from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import *

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("orderItem", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("paymob-callback/", PaymobCallbackViewSet.as_view(), name="paymob-callback"),
    # path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    # path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
]
