
import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .models import *

User = get_user_model()


class Coupon(BaseModel):
    DISCOUNT_TYPE_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    minimum_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        return self.active and self.start_date <= timezone.now() <= self.end_date and (
            self.usage_limit is None or self.usage_count < self.usage_limit
        )

    def apply_discount(self, total_amount):
        if self.discount_type == 'amount':
            return total_amount - self.discount_amount
        elif self.discount_type == 'percentage':
            return total_amount * (1 - self.discount_amount / 100)
        return total_amount

    def generate_code(self, length=6):
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not Coupon.objects.filter(code=code).exists():
                return code


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)
