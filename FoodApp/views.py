from datetime import timedelta

import stripe
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import FoodItem, FoodReview, CartItem, Cart, OrderItem, Order, Category
from .serializers import FoodItemSerializer, FoodReviewSerializer, OrderItemSerializer, OrderSerializer, \
    CartItemSerializer, CartSerializer, CategorySerializer
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from YummyFood import settings


class FoodItemView(ModelViewSet):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return FoodItem.objects.filter(category=category)
        else:
            return FoodItem.objects.all()


class FoodReviewViewSet(ModelViewSet):
    serializer_class = FoodReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        food = self.request.query_params.get('food')
        if food:
            return FoodReview.objects.filter(foodname=food)
        else:
            return FoodReview.objects.all()

    def perform_create(self, serializer):
        # Ensure reviewer matches authenticated user
        serializer.save(reviewer=self.request.user)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return the user's cart
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, pk=None):
        # Retrieve cart details with cart items
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        serializer.data['cart_items'] = CartItemSerializer(
            cart.cart_items.all(), many=True).data
        return Response(serializer.data)

    def perform_create(self, request):
        # Cart creation is handled automatically
        return Response({'message': 'Cart already exists'}, status=status.HTTP_400_BAD_REQUEST)


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        food = serializer.validated_data['food']
        cart, created = Cart.objects.get_or_create(user=user)  # Get or create cart

        # Check for existing cart item and stock availability
        if CartItem.objects.filter(cart=cart, food=food).exists():
            raise ValidationError({'message': 'Item already in cart'})
        if food.in_stock < serializer.validated_data['quantity']:
            raise ValidationError({'message': 'insufficient stock'})
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        # Check updated quantity against remaining stock
        updated_quantity = serializer.validated_data['quantity']
        food = serializer.instance.food
        if updated_quantity > food.in_stock:
            raise ValidationError({'message': 'Insufficient stock!'})

        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm("myapp.editing_access"):
            queryset = Order.objects.all().order_by('-created_date')
            return queryset
        else:
            queryset = Order.objects.filter(user=self.request.user).order_by('-created_date')
            return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        payment_method = self.request.query_params.get('payment')

        if serializer.is_valid():
            user = request.user

            cart = Cart.objects.get(user=user)
            if not cart.cart_items.all():
                return Response({'error': 'There are no items in your cart.'}, status=status.HTTP_400_BAD_REQUEST)

            # Handle order data and create order
            order = serializer.save(user=user)

            # Create OrderItems from CartItems
            for cart_item in cart.cart_items.all():
                food = FoodItem.objects.get(pk=cart_item.food.id)
                food.in_stock -= cart_item.quantity
                food.sale_count += cart_item.quantity
                food.save()
                OrderItem.objects.create(
                    order=order,
                    food=cart_item.food,
                    quantity=cart_item.quantity,
                )
                order.total_amount += (cart_item.quantity * cart_item.food.price)
            order.save()

            # Delete CartItems
            cart.cart_items.all().delete()

            if payment_method and payment_method != 'cod':
                stripe.api_key = settings.STRIPE_SECRET_KEY
                total_amount_in_cents = int(order.total_amount * 100)

                try:
                    # Create a PaymentIntent with confirmation (custom flow)
                    payment_intent = stripe.PaymentIntent.create(
                        amount=total_amount_in_cents,
                        currency='usd',
                        metadata={
                            'order_id': order.id,
                            'user': user
                        }
                    )
                    return Response({"client_secret": payment_intent.client_secret, 'data': payment_intent.metadata})
                except stripe.error.StripeError as e:
                    return Response({"error": e.error.message}, status=400)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_KEY
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    payment_intent = event['data']['object']
    order_id = payment_intent['metadata'].get('order_id')

    if event['type'] == 'payment_intent.succeeded':
        try:
            order = Order.objects.get(pk=order_id)
            if order.payment_status == 'cod':
                order.payment_status = 'paid'
                order.save()

                # Add any additional logic here to process the successful payment
                # (e.g., sending notifications, updating inventory)

                return JsonResponse({'message': 'Payment successful!'})

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    # Handle other relevant events if needed (e.g., payment_intent.canceled)
    if event['type'] == 'payment_intent.canceled':
        try:
            order = Order.objects.get(pk=order_id)
            order.status = 'cancelled'
            order.save()

            order_items = OrderItem.objects.filter(order=order.id)

            for item in order_items:
                item.food.in_stock += item.quantity

            return JsonResponse({'message': 'Order Cancelled!'})

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return JsonResponse({'message': 'Webhook received'})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, permissions.IsAuthenticatedOrReadOnly]
