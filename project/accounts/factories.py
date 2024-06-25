# -*- coding: utf-8 -*-
# myapp/factories.py
import os
import random

import factory
from accounts.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from faker.providers import BaseProvider

User=get_user_model()
fake = Faker()

data_dir = os.path.dirname(os.path.dirname(settings.BASE_DIR))
data_dir=os.path.join(data_dir,'old/data')

class ArabicNameProvider(BaseProvider):
    def  arabic_name(self):
        [
            "محمد", "علي", "أحمد", "عمر", "يوسف",
            "خالد", "حسن", "مصطفى", "حسام", "محمود",
            "سعيد", "طارق", "عبد الله", "عليّ", "ماجد",
            "جمال", "وليد", "مروان", "ناصر", "رشيد",
            "حسين", "سليمان", "عبدالرحمن", "فارس", "ياسر",
            "عليان", "رامي", "خضر", "طلال",
            "حازم", "أسامة", "منصور", "مالك", "نواف",  "شريف", "أيمن"
        ]
        arabic_names_same=[
            "أسامة","أسامه","اسامه","اسَامه","احمد","أحمد","أمين","امين","إياد","إياد","أكرم","اكرم"
        ]

        arabic_names = [ "نور", "إحسان","جهاد",",وسام","اسلام","أسلام","اسلام","احسان"]



        " ".join(random.choice(arabic_names_same) for _ in range(3))
        first=random.choice(arabic_names)
        return first


class AddressProvider(BaseProvider):
    def  address(self):
        egyptian_village_names = [
            "الدلجا",
            "كفر الشيخ",
            "بركة السبع",
            "قلوص",
            "الشهداء",
            "سمسطا",
            "دمنهور",
            "كفر الشيخ الجديدة",
            "بدر",
            "برمبال",
            "كفر المنجوم",
            "النوبارية",
            "الرياض",
            "البيضاء",
            "الرزايقة",
            "قرية النيل",
            "دسوق",
            "كفر البطيخ",
            "أبو النمرس",
            "أبو حمص"
        ]

        return  "".join([random.choice(egyptian_village_names) for i in range(3)])

class Specialization(BaseProvider):
    def specialization(self):
        elements = ["Family Medicine", "Internal Medicine",
                                                 "Pediatrics", "Surgery",
                                                 "Obstetrics and Gynecology", "Psychiatry",
                                                 "Radiology", "Emergency Medicine",
                                                    "Neurology", "Cardiology"]
        return random.choice(elements)
factory.Faker.add_provider(Specialization)

factory.Faker.add_provider(ArabicNameProvider)
factory.Faker.add_provider(AddressProvider)


class PhoneProvider(BaseProvider):
    def phone_number(self):

        prefixes = ['010', '015', '011']
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + number

factory.Faker.add_provider(PhoneProvider)



def generate_doctor_image():
     folder_path=os.path.join(data_dir,'doctor')
     result=[]
     if os.path.exists(folder_path):
        image_files = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        result= [img for img in image_files]
        if not result:
            return
        with open(os.path.join(folder_path,result[0]), "rb") as file:
            image_content = file.read()
        random.shuffle(result)
        return SimpleUploadedFile(result[0], image_content)

class DoctoerFactory(factory.Factory):
    class Meta:
        model = Doctor

    location = factory.Faker("address")
    approved = factory.Faker("boolean")
    price_for_reservation=factory.Faker("random_int", min=100, max=1000)
    specialization = factory.Faker("specialization")
    first_name =  factory.Faker( "arabic_name")
    last_name = factory.Faker("arabic_name" )
    @factory.lazy_attribute
    def image(self):
            # image=get_images(self.name,os.path.join(data_dir,'catagory'))
        return generate_doctor_image()

class UserFactory(factory.Factory):
    class Meta:
        model=User
    username = factory.Sequence(lambda n: f'user{n+User.objects.count()}')  # Unique usernames like 'user1', 'user2', ...
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')  # Unique emails based on username
