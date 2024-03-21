# -*- coding: utf-8 -*-
# myapp/management/commands/create_sample_data.py
from itertools import cycle

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from products.factories import *

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **options):
        products = Product.objects.all()

        discounts = DiscountFactory.create_batch(
            len(products),
            product=factory.Iterator(cycle(products)),
        )
        for discount in discounts:
            discount.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created and saved {len(discounts)} discounts"
            )
        )
