# myapp/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand

from products.factories import CategoryFactory, ProductFactory, OrderItemFactory , DiscountFactory
from orders.factories import OrderFactory 
from pharmacy.factories import PharmacyFactory
class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create and save sample data for Category
        categories = CategoryFactory.create_batch(5)
        for category in categories:
            category.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(categories)} categories'))
        # Create and save sample data for Pharmacy
        pharmacies = PharmacyFactory.create_batch(5)
        for pharmacy in pharmacies:
            pharmacy.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(pharmacies)} pharmacies'))

     
        products = ProductFactory.create_batch(10)
        for product in products:
            product.category.save()  
            product.pharmacy.save()
            product.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(products)} products'))

        # Create sample data for Discount
        discounts = DiscountFactory.create_batch(5)
        for discount in discounts:
            discount.product.pharmacy.save()  
            discount.product.category.save()
            discount.product.save()
            discount.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(discounts)} discounts'))
 
        # Create and save sample data for Order
        orders = OrderFactory.create_batch(3)
        for order in orders:
            # order.patient.save()
            order.pharmacy.save()
            order.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(orders)} orders'))


        # Create sample data for OrderItem
        order_items = OrderItemFactory.create_batch(10)
        for order_item in order_items:
            order_item.product.pharmacy.save()  
            order_item.product.category.save()
            order_item.product.save()

            order_item.order.pharmacy.save()
            order_item.order.save()

            order_item.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(order_items)} order items'))