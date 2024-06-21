# -*- coding: utf-8 -*-
import random
import string
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()



class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category_images", null=True, blank=True)






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




class ProductRating(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    review = models.TextField(blank=True, null=True)


    class Meta:
        unique_together = ('user', 'product')


    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'





class Coupon(BaseModel):
    DISCOUNT_TYPE_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES,blank=True, null=True)
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








class ProductImage(BaseModel):

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    priority = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.product.name



class Wishlist(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Product, related_name='wishlists', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.name if self.name else "Wishlist"}'

    class Meta:
        unique_together = ('user', 'name')
