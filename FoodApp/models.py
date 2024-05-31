from django.db import models
from UserApp.models import MyUser, UserAddress

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_CHOICES = [
    ('paid', 'Paid'),
    ('cod', 'Cash On Delivery'),
    ('pending', 'Payment is pending'),
    ('failed', 'Payment failed'),
    ('refunded', 'Payment is Refunded')
]


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category", unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    category = models.ForeignKey(Category, related_name="foods", on_delete=models.CASCADE, null=True, blank=True, default="Snacks")
    name = models.CharField(max_length=255, verbose_name='Food Name')
    price = models.FloatField(max_length=128, verbose_name="Price")
    details = models.TextField(max_length=600, verbose_name="Description")
    image = models.ImageField(upload_to="images/foods")
    in_stock = models.IntegerField(verbose_name="In stock")
    sale_count = models.IntegerField(verbose_name="Sale Count", default=0, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.name


class FoodReview(models.Model):
    foodname = models.ForeignKey(FoodItem, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(MyUser, related_name="reviews", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/reviews")
    rating = models.FloatField(max_length=5)
    review = models.TextField(max_length=600, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.foodname.name


class Cart(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return self.user.fullname


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, related_name="food_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.food.name


class Order(models.Model):
    user = models.ForeignKey(MyUser, related_name="user_orders", on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Order Status", default='pending')
    payment = models.CharField(max_length=32, choices=PAYMENT_CHOICES, verbose_name="Payment Status", default='cod')
    total_amount = models.FloatField(blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.food.name
