# -*- coding: utf-8 -*-
# myapp/factories.py
import os
import random

import factory
from django.conf import settings
from faker import Faker
from faker.providers import BaseProvider

from project.accounts.models import *

fake = Faker()

data_dir = os.path.dirname(os.path.dirname(settings.BASE_DIR))
data_dir=os.path.join(data_dir,'old/data')



class PhoneProvider(BaseProvider):
    def phone_number(self):

        prefixes = ['010', '015', '011']
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + number

factory.Faker.add_provider(PhoneProvider)



def generate_pharmacy_image(item_name):
     folder_path=os.path.join(data_dir,'pharmacy')
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
        return image_content

class DoctoerFactory(factory.Factory):
    class Meta:
        model = Doctor

    name = factory.Faker("company")
    location = factory.Faker("address")
    open_time = factory.Faker("time_object")
    close_time = factory.Faker("time_object")
    phone = factory.Faker('phone_number')
    @factory.lazy_attribute
    def image(self):
            # image=get_images(self.name,os.path.join(data_dir,'catagory'))
        return generate_pharmacy_image(self.name)
