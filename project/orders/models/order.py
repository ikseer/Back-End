from .models import *


class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',null=True,blank=True)
    items = models.ManyToManyField("products.Product", through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    owner = models.CharField(max_length=255,  null=True, blank=True)
    location= models.CharField(max_length=255, null=True, blank=True)
    phone=models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pharmacy = models.ForeignKey(
        "pharmacy.Pharmacy", on_delete=models.SET_NULL, null=True, blank=True
    )


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"


    def remove_items(self):
        order_items = self.order_items.all()
        for item in order_items:
            product = item.product
            product.stock -= item.quantity
            product.number_of_sales+=item.quantity
            product.save()

        #     item.delete()
        #  for item in self.items:
        #       product=item.product
        #       product.stock-=item.qquantity
        #       product.save()

class OrderItem(BaseModel):

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity of the product")

    def __str__(self):
            return f"{self.quantity} of {self.product.name} in Order #{self.order.id}"
