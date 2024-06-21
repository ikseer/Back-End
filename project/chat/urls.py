# myproject/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConservationViewSet, FCMTokenViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conservations', ConservationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'fcm-token',FCMTokenViewSet, basename='fcm-token')
urlpatterns = [
    path('', include(router.urls)),
]
