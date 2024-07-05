# -*- coding: utf-8 -*-
from django.urls import include, path
from products.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("category", CategoryViewSet)
router.register("product", ProductViewSet)
router.register("discount", DiscountViewSet)
router.register("product_image", ProductImageViewSet)
router.register("product_rating", ProductRatingViewSet)
# router.register("wishlist", WishlistViewSet)
router.register("home", HomeView)
router.register("coupon", CouponViewSet)
router.register(r'wishlistitem', WishlistItemViewSet)  # Register the WishlistItem viewset

urlpatterns = [
    path("", include(router.urls)),
    # path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    # path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
]
