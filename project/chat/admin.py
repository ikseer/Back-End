
# Register your models here.
from chat.models import *
from django.contrib import admin

admin.site.register(Conservation)
admin.site.register(Message)
admin.site.register(FCMToken)
admin.site.register(MessageSeenStatus)
