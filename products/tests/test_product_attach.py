from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pharmacy.models import *
from products.models import *

User = get_user_model()
import os

from django.core.files.uploadedfile import SimpleUploadedFile


def create_image_test():
    if os.path.exists("test_image.jpg"):
        return
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (150, 150)], fill="red")
    image.save("test_image.jpg")
    image.show()


class ProductAttachTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="test_admin", email="test2@example.com", password="test_password"
        )
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test2@example.com", "password": "test_password"}
        )
        self.admin_token = response.data["access"]
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        # response = self.client.post(url, {'email':  'test@example.com', 'password': 'test_password'})
        # self.user_token=response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        self.category = Category.objects.create(name="Test Category")
        self.pharmacy = Pharmacy.objects.create(name="Test Pharmacy")
        self.product = Product.objects.create(
            name="Test Product",
            price=20.0,
            strength=5,
            category=self.category,
            pharmacy=self.pharmacy,
        )

    def test_product_image_upload(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        url = "/products/product_image/"

        create_image_test()
        with open("test_image.jpg", "rb") as img:
            data = {
                "product": self.product.id,
                "image": SimpleUploadedFile(
                    "test_image.jpg", img.read(), content_type="image/jpeg"
                ),
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # delete the image
        image_id = response.data["id"]
        url = f"/products/product_image/{image_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        os.remove("test_image.jpg")

    #     data = {
    #         'product': self.product.id,
    #         'image': 'test_image2.jpg'
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     url='/products/product_image/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 2)

    #     # delete the image
    #     image_id = response.data[0]['id']
    #     url = f'/products/product_image/{image_id}/'
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_rating(self):
        # edit the rating
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        url = "/products/product_rating/"
        data = {
            "product": self.product.id,
            "rating": 4,
            "comment": "test comment",
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "product": self.product.id,
            "rating": 3,
            "comment": "test  quick comment",
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get the rating
        url = "/products/product_rating/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # edit the rating
        rating_id = response.data[0]["id"]
        url = f"/products/product_rating/{rating_id}/"
        data = {"rating": 5}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)

        # delete the rating
        url = f"/products/product_rating/{rating_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wishlist(self):
        # edit the wishlist
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        url = "/products/wishlist/"
        data = {"product": self.product.id, "user": self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get the wishlist
        url = "/products/wishlist/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # delete the wishlist
        wishlist_id = response.data[0]["id"]
        url = f"/products/wishlist/{wishlist_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
