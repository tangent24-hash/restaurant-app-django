from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodItemView,FoodReviewViewSet, CartViewSet, CartItemViewSet, OrderViewSet, webhook


router = DefaultRouter(trailing_slash=False)
router.register(r'foods', FoodItemView, basename="food")
router.register(r'reviews', FoodReviewViewSet, basename='review')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart_items', CartItemViewSet, basename='cart_item')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('payment-webhook-stripe', webhook, name='stripe_webhook')

]
