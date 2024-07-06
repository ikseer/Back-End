# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from accounts.models import *


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        # exclude = ['is_completed','image']
        fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains", "istartswith"],
            # "date_of_birth": ["exact"],
            "gender": ["exact"],
            "timezone": ["exact"],
            "user__email": ["exact"],
            "user__username": ["exact"],
            "user__id": ["exact"],
        }
