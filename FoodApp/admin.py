from django.contrib import admin
from .models import FoodItem, FoodReview, Cart, CartItem, Order, OrderItem, Category

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(FoodReview)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)