# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from shortuuid.django_fields import ShortUUIDField

User = get_user_model()


class Category(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category_images", null=True, blank=True)


class Discount(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    percentage = models.IntegerField(help_text="Percentage of discount")
    # product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    product = models.OneToOneField("products.Product", on_delete=models.CASCADE)
    start_date = models.DateField(
        null=True, blank=True, help_text="Start date of the discount"
    )
    end_date = models.DateField(
        null=True, blank=True, help_text="End date of the discount"
    )


class Product(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

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
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    pharmacy = models.ForeignKey("pharmacy.Pharmacy", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    priority = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.product.name


class ProductRating(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product.name


class Wishlist(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
class  Coupon(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    product=models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, blank=True)
    number=models.IntegerField(null=True, blank=True)
    active=models.BooleanField(default=True)
    code=ShortUUIDField(unique=True, length=8 ,max_length=22,editable=False)
    percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)] )
    start_date = models.DateField()
    end_date = models.DateField()
    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         self.code = self.generate_code()
        # super().save(*args, **kwargs)
    def __str__(self):
        return self.code
