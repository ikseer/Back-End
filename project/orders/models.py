# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class BaseModel(models.Model):

    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(BaseModel):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )



    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pharmacy = models.ForeignKey(
        "pharmacy.Pharmacy", on_delete=models.SET_NULL, null=True, blank=True
    )
    products = models.ManyToManyField(
        "products.Product", through="orders.OrderItem", related_name="products"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    # def __str__(self):
    #     return self.customer.first_name


class OrderItem(BaseModel):

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity of the product")

    def __str__(self):
        return self.product.name
class PaymobOrder(BaseModel):
    # order=models.ForeignKey("orders.Order",on_delete=models.CASCADE)
    order=models.OneToOneField("orders.Order",on_delete=models.CASCADE)
    paymob_order_id=models.CharField(max_length=255)
    paid=models.BooleanField(default=False)
    amount_cents=models.FloatField(default=0)
    currency=models.CharField(max_length=255,default="EGP")



    def __str__(self):
        return self.order.customer.username





class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', through='CartItem',related_name='items')
    def get_items(self):
        return self.cartitem_set.select_related('product')
class CartItem(BaseModel):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity of the product")
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
