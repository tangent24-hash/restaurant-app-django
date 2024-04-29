from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAddressView, UserDetailView

router = DefaultRouter(trailing_slash=False)

router.register(r'addresses', UserAddressView, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('mydetails', UserDetailView.as_view()),
]
