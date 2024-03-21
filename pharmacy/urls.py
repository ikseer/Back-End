# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"pharmacy", PharmacyViewSet, basename="pharmacy")

urlpatterns = [
    path("", include(router.urls)),
]
