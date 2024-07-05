from django.contrib.auth import get_user_model
from django.test import TestCase
from pharmacy.models import Pharmacy
from products.models import Product, WishlistItem
from products.models.category import Category
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()
class WishlistItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.category = Category.objects.create(name="Test Category1")

                # self.product = Product.objects.create(name='Test Product', price=100)
        self.pharmacy = Pharmacy.objects.create(name="Test Pharmacy")

        self.product = Product.objects.create(
                    name="Test Product",
                    price=20.0,
                    strength=5,
                    category=self.category,
                    pharmacy=self.pharmacy,
                )
        self.wishlist_item = WishlistItem.objects.create(user=self.user, product=self.product)

        self.user_token = self.get_token(self.user)
        self.user2_token = self.get_token(self.user2)
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_client(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_wishlist_item_str(self):
        self.assertEqual(str(self.wishlist_item), 'Test Product in cart of testuser')

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            WishlistItem.objects.create(user=self.user, product=self.product)

    def test_get_wishlist_items_authenticated_user(self):
        self.auth_client(self.user_token)

        response = self.client.get('/products/wishlistitem/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], self.product.id)

    def test_get_wishlist_items_unauthenticated_user(self):
        response = self.client.get('/products/wishlistitem/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wishlist_items_different_user(self):
        self.auth_client(self.user2_token)

        response = self.client.get('/products/wishlistitem/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_create_wishlist_item(self):
        self.auth_client(self.user2_token)

        response = self.client.post('/products/wishlistitem/', {'user': self.user2.id, 'product': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistItem.objects.count(), 2)

    def test_create_wishlist_item_duplicate(self):
        self.auth_client(self.user_token)

        response = self.client.post('/products/wishlistitem/', {'user': self.user.id, 'product': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_wishlist_item(self):
        self.auth_client(self.user_token)

        response = self.client.delete(f'/products/wishlistitem/{self.wishlist_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WishlistItem.objects.count(), 0)

    def test_update_wishlist_item(self):
        self.auth_client(self.user_token)

        new_product =  Product.objects.create(
                    name="Test Product",
                    price=20.0,
                    strength=5,
                    category=self.category,
                    pharmacy=self.pharmacy,
                )
        response = self.client.patch(f'/products/wishlistitem/{self.wishlist_item.id}/', {'product': new_product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wishlist_item.refresh_from_db()
        self.assertEqual(self.wishlist_item.product.id, new_product.id)
