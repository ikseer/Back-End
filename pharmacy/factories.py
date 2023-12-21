# myapp/factories.py

import factory
import io
from faker import Faker
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from pharmacy.models import Pharmacy
import os
import random
fake = Faker()

def generate_image():
    file_path='test_data/images/pharmacy'
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
    image = Image.new('RGB', (100, 100), 'rgb(0, 255, 0)')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    return SimpleUploadedFile("image.jpg", buffer.getvalue())

class PharmacyFactory(factory.Factory):
    class Meta:
        model = Pharmacy

    name = factory.Faker('company')
    location = factory.Faker('address')
    image = factory.LazyFunction(generate_image)
    open_time = factory.Faker('time_object')
    close_time = factory.Faker('time_object')
    phone = factory.Faker('phone_number')
