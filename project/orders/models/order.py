from .models import *


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',null=True,blank=True)
    items = models.ManyToManyField("products.Product", through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pharmacy = models.ForeignKey(
        "pharmacy.Pharmacy", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"


class OrderItem(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity of the product")

    def __str__(self):
            return f"{self.quantity} of {self.product.name} in Order #{self.order.id}"
