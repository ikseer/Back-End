# -*- coding: utf-8 -*-
from accounts.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(PhoneModel)
admin.site.register(Patient)
admin.site.register(Doctor)


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "image",
#         "bio",
#         "first_name",
#         "last_name",
#         "date_of_birth",
#         "gender",
#         "is_completed",
#         "timezone",
#     )


# admin.site.register(Profile, ProfileAdmin)
