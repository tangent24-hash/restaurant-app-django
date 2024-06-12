from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from .models import UserAddress, MyUser
from FoodApp.models import Cart
from dj_rest_auth.serializers import PasswordResetSerializer
from .forms import CustomPasswordResetForm


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'country', 'postal_code', 'address', 'is_default')

    def validate(self, attrs):
        # Check if the user is authenticated
        if not self.context.get('request').user.is_authenticated:
            raise ValidationError(
                'You must be logged in to create an address.')

        # Automatically set the user field based on the authenticated user
        attrs['user'] = self.context.get('request').user
        return attrs

    def create(self, validated_data):
        """Save the new UserAddress instance."""
        return UserAddress.objects.create(**validated_data)


class CustomRegisterSerializer(RegisterSerializer):
    fullname = serializers.CharField(max_length=64)
    mobile = serializers.CharField(max_length=16, required=False)
    facebook_id = serializers.CharField(max_length=255, required=False)
    date_of_birth = serializers.DateField(required=False)

    def save(self, request):
        user = super().save(request)
        # Set custom field value
        user.fullname = self.validated_data['fullname']
        user.mobile = self.validated_data['mobile']
        user.facebook_id = self.validated_data['facebook_id']
        user.date_of_birth = self.validated_data['date_of_birth']
        user.save()  # Save the user instance
        Cart.objects.create(
            user=user
        )
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id', 'email', 'fullname', 'profile_pic', 'bio', 'facebook_id', 'date_of_birth', 'account_creation_date',
            'last_login', 'is_staff')
        readable_fields = ['account_creation_date', 'is_staff']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user self-update, allowing modification of specific fields.
    """

    class Meta:
        model = MyUser
        fields = (
            'id', 'email', 'fullname', 'profile_pic', 'bio', 'facebook_id', 'date_of_birth')

    def update(self, instance, validated_data):
        """
        Custom update method to modify allowed fields.
        """
        user = instance
        user.email = validated_data.get('email', user.email)
        user.fullname = validated_data.get('fullname', user.fullname)
        user.mobile = validated_data.get('mobile', user.mobile)
        user.profile_pic = validated_data.get('profile_pic', user.profile_pic)
        user.bio = validated_data.get('bio', user.bio)
        user.facebook_id = validated_data.get('facebook_id', user.facebook_id)
        user.date_of_birth = validated_data.get(
            'date_of_birth', user.date_of_birth)
        user.save()
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomPasswordResetForm

    def get_email_options(self):
        return {
            "email_template": "account/email/password_reset_key",
            "extra_email_context": {"site_name": 'Yummy Food'},
        }
