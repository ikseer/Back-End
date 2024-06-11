# -*- coding: utf-8 -*-
# myapp/factories.py
import os
import random

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from faker.providers import BaseProvider
from orders.models import OrderItem
from products.models import *

from .providers import *

fake = Faker()


# def generate_image(item_name,file_path):

#     if os.path.exists(file_path):

#         image_files = [
#             f
#             for f in os.listdir(file_path)
#             if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
#         ]
#         item_name+='.jpg'
#         # Choose a random image file
#         # print(image_files,item_name)
#         selected_image=""
#         if item_name in image_files:
#             idx=image_files.index(item_name)
#             selected_image=image_files[idx]
#             # print("founded2")
#         else:selected_image = random.choice(image_files)

#         # Open the selected image file and read its content
#         with open(os.path.join(file_path, selected_image), "rb") as file:
#             image_content = file.read()

#         # Return a SimpleUploadedFile with the selected image content
#         return SimpleUploadedFile(selected_image, image_content)

#     # Create a simple random image using Pillow
#     image = Image.new("RGB", (100, 100), "rgb(255, 0, 0)")
#     buffer = io.BytesIO()
#     image.save(buffer, format="JPEG")
#     return SimpleUploadedFile("image.jpg", buffer.getvalue())


# def generate_product_image(item_name):
#     return generate_image(item_name,file_path="old/data/product")




# def generate_category_image(item_name):
#      folder_path=os.path.join(data_dir,'catagory')
#      result=[]
#      if os.path.exists(folder_path):
#         image_files = [
#             f
#             for f in os.listdir(folder_path)
#             if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
#         ]
#         result= [img for img in image_files if img.startswith(item_name)]
#         if not result:return
#         with open(os.path.join(folder_path,result[0]), "rb") as file:
#             image_content = file.read()

#         return SimpleUploadedFile(result[0], image_content)
def generate_product_image(item_name,priority):
    folder_path=os.path.join(data_dir,'product')
    result=[]
    if os.path.exists(folder_path):
        image_files = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        result= [img for img in image_files if img.startswith(item_name)]

        if not result:
            return
        with open(os.path.join(folder_path,result[0]), "rb") as file:
            image_content = file.read()

        return SimpleUploadedFile(result[0], image_content)
#     pass


def get_images(file_name,folder_path=os.path.join(data_dir,'product')):
     file_name=file_name.replace(' ', '_')
     file_name=file_name.replace("'", '_')

    #  print(folder_path,file_name,'l11')
    #  full_path=os.path.join(folder_path,file_name)
     result=[]
     if os.path.exists(folder_path):
        image_files = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        # print(file_name,sorted(image_files))

        result= [img for img in image_files if img.startswith(file_name)]
        # a='Truuth_Ashwagandha_500mg_Capsule_60_s_1.jpg'
        # b="Truuth_Ashwagandha_500mg_Capsule_60's"
        # print(a.startswith(b))
        # print(result)
     return result
class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Faker("category_name")

    @factory.lazy_attribute
    def image(self):
        get_images(self.name,os.path.join(data_dir,'catagory'))



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

class ProductImageFactory(factory.Factory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory("products.factories.ProductFactory")
    # image = factory.LazyFunction(generate_product_image)
    priority = factory.Faker("random_int", min=1, max=3)
    @factory.lazy_attribute
    def image(self):
        # print('ss  ',self.product[0])
        # product=Product.objects.get(id=self.product)
        product=self.product
        priority=self.priority

        # print(product['name'],self.priority,'*****')
        # print('nnn  ',product.name ,self.priority)
        generate_product_image(product.name,priority)


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
    # @factory.post_generation
    # def generate_and_save_image(self, create, extracted, **kwargs):
    #     if not create:
    #         return

        # Generate and save image for the category

        #    for img in img_factory:
            # img.save()

        # )






class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory("products.factories.ProductFactory")
    order = factory.SubFactory("orders.factories.OrderFactory")
    quantity = factory.Faker("random_int", min=1, max=10)



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
class CouponFactory(factory.Factory):
    class Meta:
        model = Coupon
    percentage = factory.Faker("random_int", min=1, max=50)
    start_date = factory.Faker("date_between", start_date="-30d", end_date="today")
    end_date = factory.Faker("date_between", start_date="today", end_date="+30d")
    product = factory.SubFactory("products.factories.ProductFactory")
    number = factory.Faker("random_int", min=1, max=1000)
