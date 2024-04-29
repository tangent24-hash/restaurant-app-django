
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import FoodItem, FoodReview, Cart, CartItem, Order, OrderItem, STATUS_CHOICES
from UserApp.models import MyUser, UserAddress
from UserApp.serializers import UserAddressSerializer


class FoodItemSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = FoodReview.objects.filter(pk=obj.pk)
        if reviews.exists():
            return sum(review.rating for review in reviews) / len(reviews)
        return 0.0

    class Meta:
        model = FoodItem
        fields = '__all__'
        read_only_fields = ('sale_count', 'created_date')


class FoodReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_reviewer_name(self, obj):
        return obj.reviewer.fullname

    def get_average_rating(self, obj):
        reviews = FoodReview.objects.filter(foodname=obj.foodname)
        if reviews.exists():
            return sum(review.rating for review in reviews) / len(reviews)
        return 0.0

    class Meta:
        model = FoodReview
        fields = '__all__'
        read_only_fields = ('created_date',)


class CartSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.fullname

    def get_cart_items(self, obj):
        return CartItemSerializer(obj.cart_items.all(), many=True).data

    class Meta:
        model = Cart
        fields = ('id', 'name', 'cart_items')


class CartItemSerializer(serializers.ModelSerializer):
    food_name = serializers.SerializerMethodField()
    food_price = serializers.SerializerMethodField()
    food_image = serializers.SerializerMethodField()

    def get_food_name(self, obj):
        return obj.food.name

    def get_food_price(self, obj):
        return obj.food.price

    def get_food_image(self, obj):
        request = self.context.get('request')
        if obj.food.image:
            if request is not None:
                image_url = request.build_absolute_uri(obj.food.image.url)
                return image_url
            else:
                # Handle the case where request is not available (e.g., during testing)
                return obj.food.image.url
        else:
            return None  # Return None or a default image URL if no image is uploaded


    class Meta:
        model = CartItem
        fields = ('id', 'food', 'food_image', 'food_name', 'food_price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all(),
                                                 required=True)  # No filter in queryset

    def get_name(self, obj):
        return obj.user.fullname

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.order_items.all(), many=True).data

    def validate_address(self, value):
        # Validate if the selected address belongs to the user
        user = self.context.get('request').user
        if value.user != user:
            raise serializers.ValidationError('Selected address does not belong to you.')
        return value

    class Meta:
        model = Order
        fields = ('id', 'name', 'total_amount', 'address', 'status', 'created_date', 'order_items')
        read_only_fields = ['total_amount']


class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.SerializerMethodField()
    food_price = serializers.SerializerMethodField()

    def get_food_name(self, obj):
        return obj.food.name

    def get_food_price(self, obj):
        return obj.food.price

    class Meta:
        model = OrderItem
        fields = ('id', 'food_name', 'food_price', 'quantity')


class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'fullname', 'orders')
