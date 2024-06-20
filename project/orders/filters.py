# from rest_framework import filters
import django_filters as filters
from orders.models import PaymobOrder

# class PaymobOrderFilter(filters.BaseFilterBackend):
#     """
#     Custom filter backend to ensure inclusion of a required query parameter.
#     """

#     def filter_queryset(self, request, queryset, view):
#         order_id = 'order_id'  # Change this to the required parameter name
#         if order_id not in request.query_params:
#             raise ParseError(f"Missing '{order_id}' parameter in query parameters.")

#         return queryset
class PaymobFilter(filters.FilterSet):
    class Meta:
        model=PaymobOrder
        fields = "__all__"
