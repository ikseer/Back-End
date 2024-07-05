# from random import random
import random

from django.core.management.base import BaseCommand
from products.models.product import Product


class Command(BaseCommand):
    help = 'Export data from all models in the database'

    def handle(self, *args, **kwargs):
        products=Product.objects.all()
        for product in products:
            product.number_of_sales=random.randint(1, 1000)
            product.save()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created and saved "
            )
        )
