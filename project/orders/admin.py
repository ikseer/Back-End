# -*- coding: utf-8 -*-
from django.contrib import admin
from orders.models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(PaymobOrder)



class PaymobOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PaymobOrder._meta.fields]

admin.site.register(PaymobOrder, PaymobOrderAdmin)
