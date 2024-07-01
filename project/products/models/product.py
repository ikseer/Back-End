


from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .models import *

User = get_user_model()


class Product(BaseModel):

    name = models.CharField(max_length=255, help_text="Name of the medication")
    generic_name = models.CharField(
        max_length=255, help_text="Generic name of the medication"
    )
    form = models.CharField(
        max_length=255,
        help_text="Form of the medication (e.g., tablet, capsule, liquid)",
    )
    strength = models.CharField(
        max_length=255, help_text="Strength of the medication (e.g., 500mg)"
    )
    factory_company = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True,default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    pharmacy = models.ForeignKey("pharmacy.Pharmacy", on_delete=models.CASCADE)
    stock  = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    # class Meta:
        # ordering = ['-created_at']

    def get_final_price(self):
        # Calculate the final price of the product after applying any valid discounts
        final_price = self.price
        for discount in self.discounts.filter(active=True, start_date__lte=timezone.now(), end_date__gte=timezone.now()):
        # for discount in self.discounts:
            if not discount.is_valid:
                continue
        #     final_price = discount.apply_discount(final_price)
        return final_price
