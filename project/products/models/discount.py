



from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .models import *
from .product import *

User = get_user_model()

class Discount(BaseModel):
    DISCOUNT_TYPE_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES,blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product.name} - {self.discount_amount} ({self.discount_type})'

    def apply_discount(self, price):
        if self.discount_type == 'amount':
            return max(price - self.discount_amount, 0)  # Ensure price doesn't go negative
        elif self.discount_type == 'percentage':
            return max(price * (1 - self.discount_amount / 100), 0)  # Ensure price doesn't go negative
        return price

    def is_valid(self):
        return self.active and self.start_date <= timezone.now() <= self.end_date
