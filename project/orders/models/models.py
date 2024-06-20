# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class PaymobOrder(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    # order=models.ForeignKey("orders.Order",on_delete=models.CASCADE)
    order=models.OneToOneField("orders.Order",on_delete=models.CASCADE,unique=True)
    paymob_order_id=models.CharField(max_length=255)
    paid=models.BooleanField(default=False)
    amount_cents=models.FloatField(default=0)
    currency=models.CharField(max_length=255,default="EGP")

    def __str__(self):
        return self.order.customer.username
