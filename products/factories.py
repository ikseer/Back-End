# myapp/factories.py
import io
import os
import random

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from faker.providers import BaseProvider
from PIL import Image

from orders.models import OrderItem
from products.models import *

fake = Faker()


def generate_image(file_path):
    if os.path.exists(file_path):
        image_files = [
            f
            for f in os.listdir(file_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]

        # Choose a random image file
        selected_image = random.choice(image_files)

        # Open the selected image file and read its content
        with open(os.path.join(file_path, selected_image), "rb") as file:
            image_content = file.read()

        # Return a SimpleUploadedFile with the selected image content
        return SimpleUploadedFile(selected_image, image_content)

    # Create a simple random image using Pillow
    image = Image.new("RGB", (100, 100), "rgb(255, 0, 0)")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return SimpleUploadedFile("image.jpg", buffer.getvalue())


def generate_product_image():
    return generate_image(file_path="test_data/images/products")


def generate_category_image():
    return generate_image(file_path="test_data/images/products")


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    image = factory.LazyFunction(generate_category_image)


class DiscountFactory(factory.Factory):
    class Meta:
        model = Discount

    percentage = factory.Faker("random_int", min=1, max=50)
    product = factory.SubFactory("products.factories.ProductFactory")
    start_date = factory.Faker("date_between", start_date="-30d", end_date="today")
    end_date = factory.Faker("date_between", start_date="today", end_date="+30d")


class ProductCodeProvider(BaseProvider):
    def product_code(self):
        # Generate your product code logic here
        return "PROD" + "".join(str(random.randint(0, 9)) for _ in range(6))


factory.Faker.add_provider(ProductCodeProvider)


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    generic_name = factory.Faker("word")
    form = factory.Faker("word")
    strength = factory.Faker("word")
    factory_company = factory.Faker("company")
    description = factory.Faker("text")
    price = factory.Faker("random_int", min=1, max=100)
    category = factory.SubFactory(CategoryFactory)
    pharmacy = factory.SubFactory("pharmacy.factories.PharmacyFactory")
    # image = factory.LazyFunction(generate_product_image)
    quantity = factory.Faker("random_int", min=1, max=100)
    short_description = factory.Faker("text")
    code = factory.Faker("product_code")


class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory("products.factories.ProductFactory")
    order = factory.SubFactory("orders.factories.OrderFactory")
    quantity = factory.Faker("random_int", min=1, max=10)


class ProductImageFactory(factory.Factory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory("products.factories.ProductFactory")
    image = factory.LazyFunction(generate_product_image)
    priority = factory.Faker("random_int", min=1, max=3)


class ProductRatingFactory(factory.Factory):
    class Meta:
        model = ProductRating

    # user = None
    product = factory.SubFactory("products.factories.ProductFactory")
    rating = factory.Faker("random_int", min=1, max=5)
    comment = factory.Faker("text")


class WishlistFactory(factory.Factory):
    class Meta:
        model = Wishlist

    user = None
    product = factory.SubFactory("products.factories.ProductFactory")
