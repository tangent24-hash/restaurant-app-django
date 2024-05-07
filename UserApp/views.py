from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import UserAddressSerializer, UserDetailsSerializer, UserUpdateSerializer
from .models import UserAddress, MyUser
from rest_framework import permissions, generics
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserAddressView(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Custom view for retrieving and updating user details.
    """
    queryset = MyUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override get_object to retrieve the logged-in user's object.
        """
        return self.request.user

    def get_serializer_class(self):
        """
        Override get_serializer_class to use different serializers for GET and PUT/PATCH.
        """
        if self.request.method == 'GET':
            return UserDetailsSerializer
        return UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        """
        Override update to allow updates only by the user themselves and handle errors.
        """
        user = self.get_object()

        if user != request.user:
            return Response({'error': 'Unauthorized'}, status=403)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  # Raise exception for validation errors

        try:
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:  # Catch generic exception for other potential errors
            return Response({'error': str(e)}, status=500)  # Return error message and status code
