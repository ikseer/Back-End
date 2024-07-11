# -*- coding: utf-8 -*-
# filters.py
import django_filters as filters

from .models import *


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = "__all__"


class ConversationFilter(filters.FilterSet):
    class Meta:
        model = Conversation
        fields = "__all__"
