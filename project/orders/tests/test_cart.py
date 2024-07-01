# -*- coding: utf-8 -*-
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import *
from pharmacy.models import *
from products.models import *
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.user2 = User.objects.create_user(
            username="test_user2", email="test2@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=self.user,verified=True)
        # EmailAddress.objects.create(user=self.user2,verified=True)

        self.pharmacy = Pharmacy.objects.create(
            name="Test pharmacy",
            location="Test location",
            image="test_data/images/pharmacy/image.jpg",
            open_time="09:00:00",
            close_time="18:00:00",
            phone="1234567890",
        )
        self.category = Category.objects.create(name="Test category")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product1",
            description="Test description",
            price=50.00,
            pharmacy=self.pharmacy,
            stock=5
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product2",
            description="Test description",
            price=100.00,
            pharmacy=self.pharmacy,
            stock=5

        )

        self.client = APIClient()
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "test_password"}
        )
        self.access_token = response.data["access"]

    def test_get_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get("/orders/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('user',response.data,)
        self.assertEqual(Cart.objects.count(),2)
        self.assertIn('total_price',response.data)

    def test_add_cart_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get("/orders/cart/")
        cart=response.data

        data={
            'product':self.product1.id,
            'quantity':3,
            'cart':cart['id']

        }
        response = self.client.post("/orders/cart-item/",data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = self.client.get("/orders/cart/")        # print(response.data)




        data["product"]=self.product2.id
        response = self.client.post("/orders/cart-item/",data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


        response = self.client.get("/orders/cart/")
        # print(response.data['items'][0])
        # self.assertEqual(response.data['items'][0]['product_name'],"Product1")

    def test_get_cart_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        cart = self.client.get("/orders/cart/").data

        data={
            'product':self.product1.id,
            'quantity':3,
            'cart':cart['id']

        }
        response = self.client.post("/orders/cart-item/",data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = self.client.get(f"/orders/cart-item/{response.data['id']}/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # print(response.data)
        # self.assertEqual(len(response.data),1)

    def test_add_cart_items_bad(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get("/orders/cart/")
        cart=response.data

        data={
            'product':self.product1.id,
            'quantity':6,
            'cart':cart['id']

        }
        response = self.client.post("/orders/cart-item/",data=data,format='json')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)







class PermissionsCartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=self.user,verified=True)

        self.user2 = User.objects.create_user(
            username="test_user2", email="test2@example.com", password="test_password"
        )
        EmailAddress.objects.create(user=self.user2,email="test2@example.com",verified=True)
        self.pharmacy = Pharmacy.objects.create(
            name="Test pharmacy",
            location="Test location",
            image="test_data/images/pharmacy/image.jpg",
            open_time="09:00:00",
            close_time="18:00:00",
            phone="1234567890",
        )
        self.category = Category.objects.create(name="Test category")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Product1",
            description="Test description",
            price=50.00,
            pharmacy=self.pharmacy,
                        stock=10

        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Product2",
            description="Test description",
            price=100.00,
            pharmacy=self.pharmacy,
                        stock=10

        )

        self.client = APIClient()
        url = reverse("rest_login")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "test_password"}
        )
        self.access_token = response.data["access"]
        response = self.client.post(    url, {"email": "test2@example.com", "password": "test_password"})
        self.access_token2 = response.data["access"]

        cart = self.client.get("/orders/cart/",HTTP_AUTHORIZATION=f"Bearer {self.access_token}").data
        self.data={
            'product':self.product1.id,
            'quantity':3,
            'cart':cart['id']

        }

    def test_get_cart(self):

        response = self.client.get("/orders/cart/",HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/orders/cart/{response.data['id']}/",HTTP_AUTHORIZATION=f"Bearer {self.access_token2}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_item(self):
        response = self.client.post("/orders/cart-item/",data=self.data,format='json',HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"/orders/cart-item/{response.data['id']}/",HTTP_AUTHORIZATION=f"Bearer {self.access_token2}")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)






    #     self.assertIn('user',response.data,)
    #     self.assertEqual(Cart.objects.count(),2)


    # def test_add_cart_items(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
    #     response = self.client.get("/orders/cart/")
    #     cart=response.data

    #     data={
    #         'product':self.product1.id,
    #         'quantity':3,
    #         'cart':cart['id']

    #     }
    #     response = self.client.post("/orders/cart-item/",data=data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)




    #     data["product"]=self.product2.id
    #     response = self.client.post("/orders/cart-item/",data=data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    #     response = self.client.get("/orders/cart/")
    #     # print(response.data['items'][0])
    #     self.assertEqual(response.data['items'][0]['product_name'],"Product1")

    # def test_get_cart_items(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
    #     cart = self.client.get("/orders/cart/").data

    #     data={
    #         'product':self.product1.id,
    #         'quantity':3,
    #         'cart':cart['id']

    #     }
    #     response = self.client.post("/orders/cart-item/",data=data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    #     response = self.client.get(f"/orders/cart-item/{response.data['id']}/")
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     print(response.data)
