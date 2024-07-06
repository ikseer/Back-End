
import django_filters as filters
from accounts.models import *


class PhoneFilter(filters.FilterSet):
    class Meta:
        model = PhoneModel
        fields='__all__'
