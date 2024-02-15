from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
User=get_user_model()

STATUS_CHOICES=(
    ('Pending','Pending'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
)
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pharmacy = models.ForeignKey('pharmacy.Pharmacy', on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField('products.Product', through='orders.OrderItem', related_name='products')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # def __str__(self):
    #     return self.customer.first_name
class OrderItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text='Quantity of the product')
    def __str__(self):
        return self.product.name