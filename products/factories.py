# myapp/factories.py

import os
import random
from tkinter.tix import Tree
import factory
from faker import Faker
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Category, Discount, Product
from orders.models import OrderItem

fake = Faker()
import io

from PIL import Image

def generate_image(file_path):
    if os.path.exists(file_path):
        image_files = [f for f in os.listdir(file_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Choose a random image file
        selected_image = random.choice(image_files)

        # Open the selected image file and read its content
        with open(os.path.join(file_path, selected_image), 'rb') as file:
            image_content = file.read()

        # Return a SimpleUploadedFile with the selected image content
        return SimpleUploadedFile(selected_image, image_content)
    
    # Create a simple random image using Pillow
    image = Image.new('RGB', (100, 100), 'rgb(255, 0, 0)')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    return SimpleUploadedFile("image.jpg", buffer.getvalue())

def generate_product_image():
    return generate_image( file_path='test_data/images/products')
def generate_category_image():
    return generate_image( file_path='test_data/images/products')


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    image = factory.LazyFunction(generate_category_image)

class DiscountFactory(factory.Factory):
    class Meta:
        model = Discount

    percentage = factory.Faker('random_int', min=1, max=50)
    product = factory.SubFactory('products.factories.ProductFactory')
    start_date = factory.Faker('date_between', start_date='-30d', end_date='today')
    end_date = factory.Faker('date_between', start_date='today', end_date='+30d')

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    generic_name = factory.Faker('word')
    form = factory.Faker('word')
    strength = factory.Faker('word')
    factory_company = factory.Faker('company')
    description = factory.Faker('text')
    price = factory.Faker('random_int', min=1, max=100)
    category = factory.SubFactory(CategoryFactory)
    pharmacy = factory.SubFactory('pharmacy.factories.PharmacyFactory')
    image = factory.LazyFunction(generate_product_image)
    quantity = factory.Faker('random_int', min=1, max=100)

class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory('products.factories.ProductFactory')
    order = factory.SubFactory('orders.factories.OrderFactory')
    quantity = factory.Faker('random_int', min=1, max=10)
