from django.contrib.auth import get_user_model
from django.test import TestCase
from pharmacy.models import \
    Pharmacy  # Assuming there is a Product model in the products app
from products.models import Product, Wishlist, WishlistItem
from products.models.category import Category
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class WishlistModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pharmacy = Pharmacy.objects.create(name="Test Pharmacy")

        self.category = Category.objects.create(name="Test Category1")
        self.product = Product.objects.create(
                    name="Test Product",
                    price=20.0,
                    strength=5,
                    category=self.category,
                    pharmacy=self.pharmacy,
                )


    def test_wishlist_item_creation(self):
        wishlist = Wishlist.objects.create(user=self.user)
        wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=self.product)
        self.assertEqual(str(wishlist_item), 'Test Product in cart of testuser')

    def test_wishlist_item_unique_together(self):
        wishlist = Wishlist.objects.create(user=self.user)
        WishlistItem.objects.create(wishlist=wishlist, product=self.product)
        with self.assertRaises(Exception):
            WishlistItem.objects.create(wishlist=wishlist, product=self.product)

class WishlistViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)
        self.pharmacy = Pharmacy.objects.create(name="Test Pharmacy")

        self.category = Category.objects.create(name="Test Category1")
        self.product = Product.objects.create(
                    name="Test Product",
                    price=20.0,
                    strength=5,
                    category=self.category,
                    pharmacy=self.pharmacy,
                )
        self.wishlist = Wishlist.objects.get(user=self.user)
        self.wishlist_item = WishlistItem.objects.create(wishlist=self.wishlist, product=self.product)

    def test_wishlist_list_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_wishlist_list_non_staff_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user'], self.user.id)


    def test_wishlist_item_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/products/wishlistitem/', {'wishlist': self.wishlist.id, 'product': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.product2 = Product.objects.create(
                                name="Test Product2",
                                price=20.0,
                                strength=5,
                                category=self.category,
                                pharmacy=self.pharmacy,
                            )
        response = self.client.post('/products/wishlistitem/', {'wishlist': self.wishlist.id, 'product': self.product2.id})
        # print(response.data,WishlistItem.objects.all())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_wishlist_permissions(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        response = self.client.get('/products/wishlist/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from products.models import Wishlist
# from rest_framework import status
# from rest_framework.test import APIClient

# User= get_user_model()
# class WishlistViewSetTests(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#         # Create test data
#         self.wishlist1 = Wishlist.objects.create(user=self.user, name='Wishlist 1')
#         self.wishlist2 = Wishlist.objects.create(user=self.user, name='Wishlist 2')

#     def test_get_wishlists(self):
#         response = self.client.get('/products/wishlist/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 2)

#     def test_create_wishlist(self):
#         new_wishlist_data = {
#             'user': self.user.id,
#             'name': 'New Wishlist',
#         }
#         response = self.client.post('/products/wishlist/', new_wishlist_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Wishlist.objects.count(), 3)

#     def test_get_single_wishlist(self):
#         response = self.client.get(f'/products/wishlist/{self.wishlist1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Wishlist 1')

#     def test_update_wishlist(self):
#         updated_data = {
#             'name': 'Updated Wishlist Name',
#         }
#         response = self.client.patch(f'/products/wishlist/{self.wishlist1.id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Updated Wishlist Name')

#     def test_delete_wishlist(self):
#         response = self.client.delete(f'/products/wishlist/{self.wishlist1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Wishlist.objects.count(), 1)

#     def test_pagination(self):
#         for i in range(10):
#             Wishlist.objects.create(user=self.user, name=f'Wishlist {i + 3}')

#         response = self.client.get('/products/wishlist/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 12)  # Assuming default pagination limit is 10

#     def test_permission_denied(self):
#         # Create a new user without admin permissions
#         unauthorized_user = User.objects.create_user(username='unauthorized', password='testpassword')
#         unauthorized_client = APIClient()
#         unauthorized_client.force_authenticate(user=unauthorized_user)

#         response = unauthorized_client.get('/products/wishlist/')
#         self.assertEqual(len(response.data['results']), 0)
