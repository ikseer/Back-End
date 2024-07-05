
# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters
from products.models import *


class ProductFilter(filters.FilterSet):
    # top_sales = filters.BooleanFilter(method="filter_top_sales")
    have_discount = filters.BooleanFilter(method="filter_have_discount")
    too_sales= filters.NumberFilter(field_name='number_of_sales')

    class Meta:
        model = Product
        # fields = "__all__"
        fields = {
            "name": ["exact", "icontains", "istartswith"],
            "generic_name": ["exact", "icontains", "istartswith"],
            "form": ["exact", "icontains", "istartswith"],
            "strength": ["exact", "icontains", "istartswith"],
            "factory_company": ["exact", "icontains", "istartswith"],
            "category__name": ["exact", "icontains", "istartswith"],
            "category__id": ["exact"],
            "description": ["exact", "icontains", "istartswith"],
            "price": ["gte", "lte", "gt", "lt"],
            "number_of_sales": ["gte", "lte", "gt", "lt"],
            "stock": ["gte", "lte", "gt", "lt"],
            # "top_sales":["gte", "lte", "gt", "lt"],
        }

    # def filter_top_sales(self, queryset, name, value):
    #     if value:
    #         return queryset.annotate(
    #             total_quantity_sold=Sum("orderitem__quantity")
    #         ).order_by("-total_quantity_sold")
    #     return queryset

    def filter_have_discount(self, queryset, name, value):
        print('*'*20)
        if value:
            print('o'*20)

            return queryset.filter(discounts__isnull=False).distinct()
        return queryset.filter(discounts__isnull=True).distinct()






class  HomeFilter(filters.FilterSet):
    have_discount = filters.BooleanFilter(method="filter_have_discount")
    # top_sales = filters.BooleanFilter(method="filter_top_sales")
    # min_stocktop_sales = filters.NumberFilter(field_name='number_of_sales')
    too_sales= filters.NumberFilter(field_name='number_of_sales')
    class Meta:
        model = Product
        # fields = "__all__"
        fields = {
            "id":["exact"],
            "name": ["exact", "icontains", "istartswith"],
            "generic_name": ["exact", "icontains", "istartswith"],
            "factory_company": ["exact", "icontains", "istartswith"],
            "category__name": ["exact", "icontains", "istartswith"],
            "category__id": ["exact"],
            "description": ["exact", "icontains", "istartswith"],
            "price": ["gte", "lte", "gt", "lt"],
            "number_of_sales": ["gte", "lte", "gt", "lt"],
            "stock": ["gte", "lte", "gt", "lt"],
            # "top_sales":["gte", "lte", "gt", "lt"],


        }

    # def filter_top_sales(self, queryset, name, value):
    #     if value:
    #         return queryset.annotate(
    #             total_quantity_sold=Sum("orderitem__quantity")
    #         ).order_by("-total_quantity_sold")
    #     return queryset

    def filter_have_discount(self, queryset, name, value):
        print('*'*20)
        if value:

            return queryset.filter(discounts__isnull=False).distinct()
        return queryset.filter(discounts__isnull=True).distinct()
