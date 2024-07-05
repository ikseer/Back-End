# -*- coding: utf-8 -*-
from django.contrib import admin
from products.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductRating)
admin.site.register(WishlistItem)
admin.site.register(Coupon)
