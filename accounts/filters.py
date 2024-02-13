# filters.py
import django_filters as filters
from .models import *
class ProfileFilter(filters.FilterSet):
    class Meta:
        model = Profile
        # exclude = ['is_completed','image']
        fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'date_of_birth': ['exact', 'icontains', 'istartswith'],
            'gender': ['exact', 'icontains', 'istartswith'],
            'bio': ['exact', 'icontains', 'istartswith'],
            'timezone': ['exact', 'icontains', 'istartswith'],
            'user__email': ['exact', 'icontains', 'istartswith'],
            'user__username': ['exact', 'icontains', 'istartswith'],
            'user__id': ['exact', 'icontains', 'istartswith'],
        }