# myapp/management/commands/create_sample_data.py
from itertools import cycle

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from pharmacy.factories import PharmacyFactory
from products.factories import *

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **options):
        # Create and save sample data for Category
        user = User.objects.all()
        print(user)
        categories = CategoryFactory.create_batch(5)
        for category in categories:
            category.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created and saved {len(categories)} categories"
            )
        )
        # Create and save sample data for Pharmacy
        pharmacies = PharmacyFactory.create_batch(5)
        for pharmacy in pharmacies:
            pharmacy.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created and saved {len(pharmacies)} pharmacies"
            )
        )

        # products = ProductFactory.create_batch(10)
        products = ProductFactory.create_batch(10)
        for product in products:
            product.category.save()
            product.pharmacy.save()
            product.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created and saved {len(products)} products"
            )
        )

        images = ProductImageFactory.create_batch(
            20,
            product=factory.Iterator(cycle(products)),
        )

        for image in images:
            image.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created and saved {len(images)} images")
        )

        reviews = ProductRatingFactory.create_batch(
            20,
            product=factory.Iterator(cycle(products)),
            user=factory.Iterator(cycle(User.objects.all())),
        )

        for review in reviews:
            review.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created and saved {len(reviews)} reviews")
        )

        # Create sample data for Discount
        discounts = DiscountFactory.create_batch(
            5,
            product=factory.Iterator(cycle(products)),
        )
        for discount in discounts:
            discount.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created and saved {len(discounts)} discounts")
        )
        # for product in products_with_images:
        #     product.category.save()
        #     product.pharmacy.save()
        #     product.save()

        # self.stdout.write(
        # self.style.SUCCESS(
        # f"Successfully created and saved {product} products"
        # )
        # )
        #
        # products = products_with_images

        # for product in products:
        #     product.category.save()
        #     product.pharmacy.save()
        #     product.save()

        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(products)} products'))

        # Create sample data for Discount
        # discounts = DiscountFactory.create_batch(5)
        # for discount in discounts:
        #     discount.product.pharmacy.save()
        #     discount.product.category.save()
        #     discount.product.save()
        #     discount.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(discounts)} discounts'))

        # Create and save sample data for Order
        # orders = OrderFactory.create_batch(3)
        # for order in orders:
        #     # order.patient.save()
        #     order.pharmacy.save()
        #     order.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(orders)} orders'))

        # Create sample data for OrderItem
        # order_items = OrderItemFactory.create_batch(3)
        # for order_item in order_items:
        #     order_item.product.pharmacy.save()
        #     order_item.product.category.save()
        #     order_item.product.save()

        #     order_item.order.pharmacy.save()
        #     order_item.order.save()

        #     order_item.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(order_items)} order items'))

        # product_images = ProductImageFactory.create_batch(3)
        # for product_image in product_images:
        #     product_image.product.pharmacy.save()
        #     product_image.product.category.save()
        #     product_image.product.save()
        #     product_image.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(product_images)} product images'))

        # product_ratings = ProductRatingFactory.create_batch(3)
        # for product_rating in product_ratings:
        #     product_rating.product.pharmacy.save()
        #     product_rating.product.category.save()
        #     product_rating.product.save()
        #     product_rating.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(product_ratings)} product ratings'))
        # wishlists = WishlistFactory.create_batch(3)
        # for wishlist in wishlists:
        #     wishlist.product.pharmacy.save()
        #     wishlist.product.category.save()
        #     wishlist.product.save()
        #     wishlist.save()
        # self.stdout.write(self.style.SUCCESS(f'Successfully created and saved {len(wishlists)} wishlists'))

        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))
