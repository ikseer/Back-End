# myproject/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConservationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conservations', ConservationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
