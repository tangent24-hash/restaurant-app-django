from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAddressView, UserDetailView
from allauth.account.views import confirm_email
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView

router = DefaultRouter(trailing_slash=False)

router.register(r'addresses', UserAddressView, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('mydetails', UserDetailView.as_view()),
    path('account/', include('allauth.urls')),  # allauth URLs
    # path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('account-confirm-email/<str:key>/', confirm_email, name='account_confirm_email'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
