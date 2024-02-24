from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import *

router = DefaultRouter()
router.register("category", CategoryViewSet)
router.register("product", ProductViewSet)
router.register("discount", DiscountViewSet)
router.register("product_image", ProductImageViewSet)
router.register("product_rating", ProductRatingViewSet)
router.register("wishlist", WishlistViewSet)
router.register("home", HomeView)
router.register("coupon", CouponViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    # path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
]
