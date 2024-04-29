from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import UserAddress, MyUser
from FoodApp.models import Cart

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('country', 'postal_code', 'address', 'is_default')

    def validate(self, attrs):
        # Check if the user is authenticated
        if not self.context.get('request').user.is_authenticated:
            raise ValidationError('You must be logged in to create an address.')

        # Automatically set the user field based on the authenticated user
        attrs['user'] = self.context.get('request').user
        return attrs

    def create(self, validated_data):
        """Save the new UserAddress instance."""
        return UserAddress.objects.create(**validated_data)


class CustomRegisterSerializer(RegisterSerializer):
    fullname = serializers.CharField(max_length=64)
    mobile = serializers.CharField(max_length=16)
    facebook_id = serializers.CharField( max_length=255)
    date_of_birth = serializers.DateField()

    def save(self, request):
        user = super().save(request)
        user.fullname = self.validated_data['fullname']  # Set custom field value
        user.mobile = self.validated_data['mobile']
        user.facebook_id = self.validated_data['facebook_id']
        user.date_of_birth = self.validated_data['date_of_birth']
        user.save()  # Save the user instance
        Cart.objects.create(
            user=user
        )
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    Custom serializer for retrieving user details with additional fields if needed.
    """

    # Add fields from your custom user model you want to expose in the API response

    class Meta(UserDetailsSerializer.Meta):
        model = MyUser  # Use your custom user model
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    default_address = serializers.SerializerMethodField()


    class Meta:
        model = MyUser
        fields = ('id', 'email', 'account_creation_date', 'last_login', 'is_active')  # Adjust fields as needed
        # Exclude non-readable fields by default

    def to_representation(self, instance):
        """
        Overriding to_representation to include only non-writable fields.
        """
        data = super().to_representation(instance)
        # Exclude fields you don't want the user to see
        del data['is_active']  # Example: Exclude non-readable fields
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user self-update, allowing modification of specific fields.
    """

    class Meta:
        model = MyUser
        fields = ('email', 'fullname', 'mobile')  # Adjust editable fields

    def update(self, instance, validated_data):
        """
        Custom update method to modify allowed fields.
        """
        user = instance
        user.email = validated_data.get('email', user.email)
        user.fullname = validated_data.get('fullname', user.fullname)
        user.mobile = validated_data.get('mobile', user.mobile)
        user.save()
        return user
