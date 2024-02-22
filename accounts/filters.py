# filters.py
import django_filters as filters

from .models import Profile


class ProfileFilter(filters.FilterSet):
    class Meta:
        model = Profile
        # exclude = ['is_completed','image']
        fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains", "istartswith"],
            "date_of_birth": ["exact"],
            "gender": ["exact"],
            "timezone": ["exact"],
            "user__email": ["exact"],
            "user__username": ["exact"],
            "user__id": ["exact"],
        }
